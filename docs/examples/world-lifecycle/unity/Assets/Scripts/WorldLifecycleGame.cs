using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using UnityEngine;
using UnityEngine.SceneManagement;
using Debug = UnityEngine.Debug;

namespace WorldLifecycle
{
    internal enum Place { Town, LoadingForest, Forest, UnloadingForest, Failed }

    [Serializable]
    internal sealed class StreamingSample
    {
        public double requestToSceneReadyMs;
        public double largestUpdateGapMs;
        public double[] updateGapsMs;
        public int sceneObjects;
    }

    public sealed class WorldLifecycleGame : MonoBehaviour
    {
        public const float ForestX = 80;
        private const string ForestScenePath = "Assets/Generated/Forest.unity";
        private const double PatrolInterval = 0.65;
        private static readonly double MillisecondsPerTick = 1000.0 / Stopwatch.Frequency;

        private readonly List<double> updateGaps = new List<double>(128);
        private Scene town;
        private Camera worldCamera;
        private WolfView wolf;
        private AsyncOperation sceneOperation;
        private string savePath;
        private double nextPatrolAt;
        private long loadRequestedAt;
        private long sceneReadyAt;
        private long lastUpdateAt;
        private string message = "";

        internal Place Location { get; private set; } = Place.Town;
        internal WolfState State { get; private set; }
        internal WolfView View => wolf;
        internal string Error => Location == Place.Failed ? message : "";
        internal bool IsForestLoaded => SceneManager.GetSceneByPath(ForestScenePath).isLoaded;
        internal bool IsForestActive => SceneManager.GetActiveScene().path == ForestScenePath;
        internal StreamingSample LastLoad { get; private set; }

        private void Start()
        {
            if (Argument("-world-scale") is string scaleMode)
            {
                enabled = false;
                gameObject.AddComponent<LargeForestBenchmark>().Begin(scaleMode);
                return;
            }
            town = gameObject.scene;
            worldCamera = FindFirstObjectByType<Camera>();
            savePath = Argument("-world-save") ?? Path.Combine(Application.persistentDataPath, "world-v2.json");
            var report = Argument("-world-report");
            var legacyPath = Argument("-world-legacy");
            try
            {
                var input = legacyPath ?? (File.Exists(savePath) ? savePath : null);
                var embedded = input == null ? Resources.Load<TextAsset>("legacy-v1") : null;
                if (input == null && embedded == null)
                    throw new InvalidDataException("The starter save is missing. Prepare the sample in the editor.");

                State = WorldSave.Read(input == null ? embedded.text : File.ReadAllText(input));
                nextPatrolAt = Time.timeAsDouble + PatrolInterval;
            }
            catch (Exception exception)
            {
                Fail(exception);
            }

            if (report != null)
                gameObject.AddComponent<WorldLifecycleProbe>().Begin(this, savePath, report);
        }

        private void Update()
        {
            var now = Stopwatch.GetTimestamp();
            if (loadRequestedAt != 0 && lastUpdateAt != 0)
            {
                updateGaps.Add((now - lastUpdateAt) * MillisecondsPerTick);
                if (sceneReadyAt != 0)
                    FinishLoadMeasurement();
            }

            lastUpdateAt = now;
            if (Location == Place.Failed || State == null)
                return;
            if (sceneOperation != null && sceneOperation.isDone)
            {
                sceneOperation = null;
                try
                {
                    if (Location == Place.LoadingForest)
                        ActivateForest();
                    else
                        FinishReturn();
                }
                catch (Exception exception)
                {
                    Fail(exception);
                }
            }

            double gameTime = Time.timeAsDouble;
            if (Location == Place.Town && gameTime >= nextPatrolAt)
            {
                int elapsedSteps = (int)Math.Min(int.MaxValue, 1 + Math.Floor((gameTime - nextPatrolAt) / PatrolInterval));
                if (State.Hp > 0)
                    State = State.Patrol(elapsedSteps);
                nextPatrolAt += elapsedSteps * PatrolInterval;
            }
        }

        internal bool EnterForest()
        {
            if (Location != Place.Town || State == null)
                return false;

            Location = Place.LoadingForest;
            message = "Opening the forest gate...";
            LastLoad = null;
            updateGaps.Clear();
            sceneReadyAt = 0;
            loadRequestedAt = Stopwatch.GetTimestamp();
            try
            {
                sceneOperation = SceneManager.LoadSceneAsync(ForestScenePath, LoadSceneMode.Additive);
                if (sceneOperation == null)
                    throw new InvalidOperationException("Unity refused the forest load.");
                return true;
            }
            catch (Exception exception)
            {
                Fail(exception);
                return false;
            }
        }

        internal bool Strike()
        {
            if (Location != Place.Forest || wolf == null || State.Hp == 0)
                return false;

            State = State.Hit();
            wolf.Present(State);
            message = "Wolf took 40 damage.";
            return true;
        }

        internal bool ReturnToTown()
        {
            if (Location != Place.Forest || LastLoad == null)
                return false;

            Location = Place.UnloadingForest;
            message = "Returning to town...";
            try
            {
                if (!SceneManager.SetActiveScene(town))
                    throw new InvalidOperationException("Unity could not reactivate town.");
                var position = worldCamera.transform.position;
                worldCamera.transform.position = new Vector3(0, position.y, position.z);
                sceneOperation = SceneManager.UnloadSceneAsync(SceneManager.GetSceneByPath(ForestScenePath));
                if (sceneOperation == null)
                    throw new InvalidOperationException("Unity refused the forest unload.");
                return true;
            }
            catch (Exception exception)
            {
                Fail(exception);
                return false;
            }
        }

        internal bool Save()
        {
            if (Location != Place.Town && Location != Place.Forest)
                return false;

            try
            {
                WorldSave.Publish(savePath, State);
                message = "Saved the current wolf and quest state.";
                return true;
            }
            catch (IOException exception)
            {
                message = exception.Message;
                return false;
            }
            catch (UnauthorizedAccessException exception)
            {
                message = exception.Message;
                return false;
            }
        }

        internal bool TryRestore(string json)
        {
            if (Location != Place.Town)
                return false;

            try
            {
                var candidate = WorldSave.Read(json);
                State = candidate;
                nextPatrolAt = Time.timeAsDouble + PatrolInterval;
                return true;
            }
            catch (InvalidDataException exception)
            {
                message = exception.Message;
                return false;
            }
        }

        private void ActivateForest()
        {
            var forest = SceneManager.GetSceneByPath(ForestScenePath);
            if (!forest.isLoaded)
                throw new InvalidOperationException("Forest load completed without a loaded scene.");

            foreach (var root in forest.GetRootGameObjects())
            {
                if (root.TryGetComponent<WolfView>(out var view))
                {
                    if (wolf != null)
                        throw new InvalidOperationException("Forest has more than one wolf view.");
                    wolf = view;
                }
            }

            if (wolf == null || !SceneManager.SetActiveScene(forest))
                throw new InvalidOperationException("Forest is missing its wolf view or cannot become active.");

            wolf.Present(State);
            var position = worldCamera.transform.position;
            worldCamera.transform.position = new Vector3(ForestX, position.y, position.z);
            Location = Place.Forest;
            sceneReadyAt = Stopwatch.GetTimestamp();
            message = "The wolf is in the clearing.";
        }

        private void FinishLoadMeasurement()
        {
            int count = 0;
            double largest = 0;
            foreach (var root in SceneManager.GetSceneByPath(ForestScenePath).GetRootGameObjects())
                count += root.GetComponentsInChildren<Transform>(true).Length;
            foreach (var gap in updateGaps)
                largest = Math.Max(largest, gap);

            LastLoad = new StreamingSample
            {
                requestToSceneReadyMs = (sceneReadyAt - loadRequestedAt) * MillisecondsPerTick,
                largestUpdateGapMs = largest,
                updateGapsMs = updateGaps.ToArray(),
                sceneObjects = count
            };
            loadRequestedAt = 0;
            sceneReadyAt = 0;
        }

        private void FinishReturn()
        {
            if (IsForestLoaded || wolf != null)
                throw new InvalidOperationException("Forest scene or wolf survived the unload.");

            wolf = null;
            Location = Place.Town;
            nextPatrolAt = Time.timeAsDouble + PatrolInterval;
            message = "Forest unloaded. The wolf keeps patrolling.";
        }

        private void Fail(Exception exception)
        {
            Location = Place.Failed;
            sceneOperation = null;
            loadRequestedAt = 0;
            message = exception.Message;
            Debug.LogException(exception);
        }

        private void OnGUI()
        {
            GUILayout.BeginArea(new Rect(16, 16, 350, 230), GUI.skin.box);
            GUILayout.Label(Location == Place.Forest ? "Forest clearing" : "Town gate");
            if (State != null)
                GUILayout.Label($"Wolf HP {State.Hp}/100    Quest {State.QuestStage}    Patrol {State.PatrolSteps}");
            if (Location == Place.Town && State != null && GUILayout.Button("Enter forest"))
                EnterForest();
            if (Location == Place.Forest)
            {
                if (GUILayout.Button("Strike wolf"))
                    Strike();
                if (LastLoad != null && GUILayout.Button("Return to town"))
                    ReturnToTown();
            }
            if ((Location == Place.Town || Location == Place.Forest) && State != null && GUILayout.Button("Save"))
                Save();
            if (LastLoad != null)
                GUILayout.Label($"Forest ready in {LastLoad.requestToSceneReadyMs:F1} ms");
            GUILayout.Label(message);
            GUILayout.EndArea();
        }

        internal static string Argument(string key)
        {
            var args = Environment.GetCommandLineArgs();
            int index = Array.IndexOf(args, key);
            return index >= 0 && index + 1 < args.Length ? args[index + 1] : null;
        }
    }
}
