using System;
using System.Collections;
using System.Diagnostics;
using System.IO;
using UnityEngine;
using Debug = UnityEngine.Debug;

namespace WorldLifecycle
{
    internal sealed class WorldLifecycleProbe : MonoBehaviour
    {
        [Serializable]
        private sealed class Snapshot
        {
            public string catalogId;
            public int hp;
            public int questStage;
            public int patrolSteps;
            public bool forestLoaded;
            public bool forestActive;
            public int viewId;

            public Snapshot(WorldLifecycleGame game)
            {
                catalogId = game.State.Id;
                hp = game.State.Hp;
                questStage = game.State.QuestStage;
                patrolSteps = game.State.PatrolSteps;
                forestLoaded = game.IsForestLoaded;
                forestActive = game.IsForestActive;
                viewId = game.View == null ? 0 : game.View.GetInstanceID();
            }
        }

        [Serializable]
        private sealed class RunReport
        {
            public bool passed;
            public string failure;
            public string utc;
            public int pid;
            public string engine;
            public string os;
            public string graphics;
            public string graphicsApi;
            public string cpu;
            public int width;
            public int height;
            public bool batchMode;
            public int vSyncCount;
            public int targetFrameRate;
            public Snapshot initial;
            public StreamingSample firstEntry;
            public Snapshot firstView;
            public Snapshot combat;
            public Snapshot unloaded;
            public Snapshot offscreenPatrol;
            public StreamingSample revisit;
            public Snapshot rebound;
            public bool originalViewDestroyed;
            public bool malformedPreservedLiveState;
            public bool legacyAliasRejectedInV2;
            public bool unsupportedSchemaRejected;
            public string savedJson;
            public Snapshot reloaded;
        }

        private WorldLifecycleGame game;
        private string savePath;
        private string reportPath;
        private readonly RunReport report = new RunReport();

        internal void Begin(WorldLifecycleGame world, string save, string output)
        {
            game = world;
            savePath = save;
            reportPath = output;
            StartCoroutine(GuardedRun());
        }

        private IEnumerator GuardedRun()
        {
            report.utc = DateTime.UtcNow.ToString("o");
            report.pid = Process.GetCurrentProcess().Id;
            report.engine = Application.unityVersion;
            report.os = SystemInfo.operatingSystem;
            report.graphics = SystemInfo.graphicsDeviceName;
            report.graphicsApi = SystemInfo.graphicsDeviceType.ToString();
            report.cpu = SystemInfo.processorType;
            report.width = Screen.width;
            report.height = Screen.height;
            report.batchMode = Application.isBatchMode;
            report.vSyncCount = QualitySettings.vSyncCount;
            report.targetFrameRate = Application.targetFrameRate;

            var scenario = Scenario();
            var deadline = Time.realtimeSinceStartupAsDouble + 30;
            while (true)
            {
                try
                {
                    Require(Time.realtimeSinceStartupAsDouble < deadline, "Scenario exceeded 30 seconds.");
                    Require(game.Location != Place.Failed, game.Error);
                    if (!scenario.MoveNext())
                    {
                        report.passed = true;
                        break;
                    }
                }
                catch (Exception exception)
                {
                    report.failure = exception.Message;
                    Debug.LogException(exception);
                    break;
                }

                yield return null;
            }

            try
            {
                File.WriteAllText(reportPath, JsonUtility.ToJson(report, true) + Environment.NewLine);
            }
            catch (Exception exception)
            {
                Debug.LogException(exception);
                Application.Quit(2);
                yield break;
            }
            Debug.Log(report.passed ? "WORLD_LIFECYCLE_PROBE_PASS" : "WORLD_LIFECYCLE_PROBE_FAIL");
            Application.Quit(report.passed ? 0 : 1);
        }

        private IEnumerator Scenario()
        {
            report.initial = new Snapshot(game);
            Require(report.initial.catalogId == "forest-wolf-v2" && game.State.Hp == 100 &&
                game.State.QuestStage == 0 && game.State.PatrolSteps == 0 && !game.IsForestLoaded && game.View == null,
                "Legacy boot did not produce the expected town state.");
            Require(!game.Strike(), "Combat was accepted while the presentation was absent.");
            for (int frame = 0; frame < 5; frame++)
                yield return null;

            Require(game.EnterForest() && !game.EnterForest(), "Forest portal did not serialize duplicate requests.");
            while (game.LastLoad == null)
                yield return null;
            report.firstEntry = game.LastLoad;
            report.firstView = new Snapshot(game);
            var originalView = game.View;
            RequireReady();

            Require(game.Strike(), "Combat action was rejected in forest.");
            report.combat = new Snapshot(game);
            Require(game.State.Hp == 60 && game.State.QuestStage == 1, "Strike did not update combat and quest state.");
            Require(WorldSave.SameState(game.View.PresentedState, game.State), "Combat presentation was stale.");
            Require(game.ReturnToTown(), "Town portal was rejected.");
            while (game.Location != Place.Town)
                yield return null;

            report.unloaded = new Snapshot(game);
            report.originalViewDestroyed = originalView == null;
            Require(!game.IsForestLoaded && !game.IsForestActive && game.View == null && report.originalViewDestroyed,
                "Forest scene or original wolf view remained after unload.");
            var unloaded = game.State;
            while (game.State.PatrolSteps == unloaded.PatrolSteps)
                yield return null;
            report.offscreenPatrol = new Snapshot(game);
            Require(!game.IsForestLoaded && game.View == null && report.offscreenPatrol.catalogId == "forest-wolf-v2" &&
                game.State.Hp == 60 && game.State.QuestStage == 1 && game.State.PatrolSteps == unloaded.PatrolSteps + 1,
                "Authoritative wolf state did not tick exactly once while the forest was absent.");
            var expectedOnArrival = game.State;

            Require(game.EnterForest(), "Revisit was rejected.");
            while (game.LastLoad == null)
                yield return null;
            report.revisit = game.LastLoad;
            report.rebound = new Snapshot(game);
            RequireReady();
            Require(!ReferenceEquals(originalView, game.View), "Revisit reused the destroyed view.");
            Require(WorldSave.SameState(expectedOnArrival, game.View.PresentedState), "Rebound view lost offscreen state.");

            Require(game.Save(), "Saving the live snapshot failed.");
            report.savedJson = File.ReadAllText(savePath);
            Require(report.savedJson.Contains("\"schemaVersion\":2") &&
                report.savedJson.Contains("\"npcId\":\"forest-wolf-v2\""), "Rewritten save kept a legacy schema or alias.");
            Require(game.ReturnToTown(), "Second return was rejected.");
            while (game.Location != Place.Town)
                yield return null;
            while (game.State.PatrolSteps == expectedOnArrival.PatrolSteps)
                yield return null;

            var beforeInvalid = game.State;
            report.malformedPreservedLiveState = !game.TryRestore("{") && ReferenceEquals(beforeInvalid, game.State);
            report.legacyAliasRejectedInV2 = !game.TryRestore(report.savedJson.Replace("forest-wolf-v2", "forest-wolf")) &&
                ReferenceEquals(beforeInvalid, game.State);
            report.unsupportedSchemaRejected = !game.TryRestore(report.savedJson.Replace("\"schemaVersion\":2", "\"schemaVersion\":21")) &&
                ReferenceEquals(beforeInvalid, game.State);
            Require(report.malformedPreservedLiveState && report.legacyAliasRejectedInV2 && report.unsupportedSchemaRejected,
                "A bad save was accepted or mutated live state.");
            Require(File.ReadAllText(savePath) == report.savedJson, "Failed restore changed the saved file.");
            Require(game.TryRestore(File.ReadAllText(savePath)) && WorldSave.SameState(expectedOnArrival, game.State),
                "Disk reload did not reproduce the saved values.");
            report.reloaded = new Snapshot(game);
        }

        private void RequireReady()
        {
            Require(game.Location == Place.Forest && game.IsForestLoaded && game.IsForestActive && game.View != null,
                "Forest was reported ready before it and its view were active.");
            Require(WorldSave.SameState(game.View.PresentedState, game.State), "Forest view did not receive authoritative state.");
            Require(game.LastLoad.requestToSceneReadyMs > 0 && game.LastLoad.updateGapsMs.Length >= 2 &&
                game.LastLoad.largestUpdateGapMs > 0 && game.LastLoad.sceneObjects > 300,
                "The stream did not yield a complete measurement for the authored forest.");
        }

        private static void Require(bool condition, string message)
        {
            if (!condition)
                throw new InvalidOperationException(message);
        }
    }
}
