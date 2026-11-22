using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using UnityEngine;
using UnityEngine.SceneManagement;
using Debug = UnityEngine.Debug;

namespace WorldLifecycle
{
    internal sealed class LargeForestBenchmark : MonoBehaviour
    {
        private const int TargetId = 5 * NpcPopulation.PerChunk + 17;
        private const int TransitionTicks = 24;
        private const int SteadyTicks = 72;
        private static readonly double MsPerTick = 1000.0 / Stopwatch.Frequency;

        [Serializable]
        private struct FrameSample
        {
            public string phase;
            public string stage;
            public double milliseconds;
        }

        [Serializable]
        private struct MemorySample
        {
            public string stage;
            public int tick, loadedChunks;
            public double elapsedMs;
            public long privateBytes, workingSetBytes;
        }

        [Serializable]
        private struct Transition
        {
            public string stage;
            public int target, chunksAtStart, chunksAtEnd;
            public double requestToReadyMs;
        }

        [Serializable]
        private sealed class Checkpoint
        {
            public string stage;
            public int tick, loadedChunks, currentChunk, boundViews, wolfHp, wolfQuest, wolfPatrol, targetViewId;
            public long npcDigest;
            public NpcSnapshot[] npcs;
        }

        [Serializable]
        private sealed class RunReport
        {
            public bool passed, batchMode, inputUnchanged, invalidCandidatesRejected, originalTargetViewDestroyed, wolfRoundTrip;
            public string mode, engine, os, graphics, graphicsApi, cpu, fixture, failure, savedJson, utc;
            public int pid, fixtureVersion, logicalNpcs, npcUpdates, otherNpcUpdates, loads, unloads;
            public int width, height, vSync, targetFrameRate, ticks, geometryObjectsPerChunk, finalLoadedChunks, peakLoadedChunks;
            public int renderedFrames, nonBackgroundPixels;
            public FrameSample[] frameSamples;
            public MemorySample[] memorySamples;
            public Checkpoint[] checkpoints;
            public Transition[] transitions;
        }

        [StructLayout(LayoutKind.Sequential)]
        private struct WindowsMemoryCounters
        {
            public uint size, pageFaults;
            public UIntPtr peakWorkingSet, workingSet, peakPagedPool, pagedPool, peakNonpagedPool, nonpagedPool;
            public UIntPtr pagefile, peakPagefile, privateUsage;
        }

        [DllImport("kernel32.dll")]
        private static extern IntPtr GetCurrentProcess();

        [DllImport("kernel32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        private static extern bool K32GetProcessMemoryInfo(IntPtr process, ref WindowsMemoryCounters counters, uint size);

        private readonly List<FrameSample> frames = new List<FrameSample>(1024);
        private readonly List<MemorySample> memory = new List<MemorySample>(100);
        private readonly List<Transition> transitions = new List<Transition>(5);
        private readonly List<Checkpoint> checkpoints = new List<Checkpoint>(10);
        private readonly LargeForestChunk[] loaded = new LargeForestChunk[LargeForestChunk.Count];
        private readonly RunReport report = new RunReport();
        private Camera worldCamera;
        private RenderTexture renderTarget;
        private Scene town;
        private Vector3 townCameraPosition;
        private string mode, stage, phase;
        private bool stream, sampling;
        private long startedAt, lastFrameAt;
        private int currentChunk = -1, interestChunk = -1, tickLimit;
        private NpcPopulation npcs;
        private WolfState wolf;

        internal void Begin(string requestedMode)
        {
            mode = requestedMode;
            StartCoroutine(GuardedRun(Scenario()));
        }

        private IEnumerator GuardedRun(IEnumerator scenario)
        {
            var pending = new Stack<IEnumerator>();
            pending.Push(scenario);
            double deadline = Time.realtimeSinceStartupAsDouble + 80;
            while (pending.Count > 0)
            {
                try
                {
                    Require(Time.realtimeSinceStartupAsDouble < deadline, "The scale route exceeded 80 seconds.");
                    var current = pending.Peek();
                    if (!current.MoveNext())
                    {
                        pending.Pop();
                        continue;
                    }
                    if (current.Current is IEnumerator child)
                    {
                        pending.Push(child);
                        continue;
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

            sampling = false;
            report.passed = pending.Count == 0;
            report.frameSamples = frames.ToArray();
            report.memorySamples = memory.ToArray();
            report.checkpoints = checkpoints.ToArray();
            report.transitions = transitions.ToArray();
            try
            {
                string output = WorldLifecycleGame.Argument("-world-scale-report");
                Require(output != null, "Missing -world-scale-report path.");
                File.WriteAllText(output, JsonUtility.ToJson(report, false) + Environment.NewLine);
            }
            catch (Exception exception)
            {
                Debug.LogException(exception);
                Application.Quit(2);
                yield break;
            }
            Debug.Log(report.passed ? "LARGE_FOREST_PASS" : "LARGE_FOREST_FAIL");
            Application.Quit(report.passed ? 0 : 1);
        }

        private IEnumerator Scenario()
        {
            Require(mode == "resident-full" || mode == "stream-full" || mode == "resident-coarse" || mode == "stream-coarse",
                "Unknown large-forest mode.");
            stream = mode.StartsWith("stream-", StringComparison.Ordinal);
            npcs = new NpcPopulation(mode.EndsWith("-coarse", StringComparison.Ordinal));
            string input = WorldLifecycleGame.Argument("-world-legacy");
            string output = WorldLifecycleGame.Argument("-world-save");
            Require(input != null && output != null && Path.GetFullPath(input) != Path.GetFullPath(output), "Supply separate input and output slots.");
            var inputBytes = File.ReadAllBytes(input);
            wolf = WorldSave.Read(File.ReadAllText(input));
            bool isV1 = WorldLifecycleGame.Argument("-world-scale-fixture") == "1";
            Require(wolf.Id == "forest-wolf-v2" && wolf.Hp == (isV1 ? 100 : 60) &&
                wolf.QuestStage == (isV1 ? 0 : 1) && wolf.PatrolSteps == (isV1 ? 0 : 1), "Fixture did not restore its expected values.");

            town = gameObject.scene;
            worldCamera = FindFirstObjectByType<Camera>();
            townCameraPosition = worldCamera.transform.position;
            Require(SystemInfo.graphicsDeviceType == UnityEngine.Rendering.GraphicsDeviceType.Direct3D11,
                "The benchmark requires a Direct3D 11 graphics device.");
            renderTarget = new RenderTexture(1280, 720, 24, RenderTextureFormat.ARGB32) { name = "Benchmark render target" };
            Require(renderTarget.Create(), "Could not allocate the benchmark render target.");
            worldCamera.targetTexture = renderTarget;
            worldCamera.enabled = false;
            QualitySettings.vSyncCount = 0;
            Application.targetFrameRate = -1;
            Application.runInBackground = true;
            report.mode = mode;
            report.fixture = Path.GetFileName(input);
            report.fixtureVersion = isV1 ? 1 : 2;
            using (var process = Process.GetCurrentProcess())
                report.pid = process.Id;
            report.engine = Application.unityVersion;
            report.os = SystemInfo.operatingSystem;
            report.cpu = SystemInfo.processorType;
            report.graphics = SystemInfo.graphicsDeviceName;
            report.graphicsApi = SystemInfo.graphicsDeviceType.ToString();
            report.utc = DateTime.UtcNow.ToString("o");
            report.batchMode = Application.isBatchMode;
            report.width = renderTarget.width;
            report.height = renderTarget.height;
            report.vSync = QualitySettings.vSyncCount;
            report.targetFrameRate = Application.targetFrameRate;
            report.logicalNpcs = NpcPopulation.Total;

            for (int i = 0; i < 20; i++)
                yield return null;

            SetPhase("preload", "initialPreload");
            startedAt = Stopwatch.GetTimestamp();
            sampling = true;
            SampleMemory("beforePreload");
            if (!stream)
            {
                for (int i = 0; i < loaded.Length; i++)
                    yield return Load(i);
            }
            else
            {
                yield return null;
            }
            SampleMemory("afterPreload");
            SaveCheckpoint("initial", stream ? 0 : loaded.Length);
            yield return Dwell("townBefore");
            yield return Travel(0, "toChunk0");
            yield return Dwell("chunk0");
            yield return Travel(2, "toChunk2");
            yield return Dwell("chunk2");
            yield return Travel(5, "toChunk5");
            yield return Dwell("chunk5");

            var originalTargetView = loaded[5];
            int combatViewId = originalTargetView.ViewIdFor(TargetId);
            int previousHp = wolf.Hp;
            wolf = wolf.Hit();
            npcs.Strike(TargetId);
            loaded[5].Present(npcs, wolf);
            var hit = npcs.Observe(TargetId);
            Require(wolf.Hp == previousHp - 40 && wolf.QuestStage == 1 && hit.hp == 65 && SameNpc(originalTargetView.Presented(TargetId), hit),
                "Combat mutation or its view was incorrect.");
            SaveCheckpoint("combat", stream ? 1 : loaded.Length);

            yield return Travel(-1, "returnTown");
            report.originalTargetViewDestroyed = originalTargetView == null;
            Require(report.originalTargetViewDestroyed == stream && SceneManager.GetSceneByPath(LargeForestChunk.ScenePath(5)).isLoaded == !stream,
                "Return-to-town chunk and view residence did not match the selected mode.");
            var absentStart = npcs.Observe(TargetId);
            SaveCheckpoint("townArrival", stream ? 0 : loaded.Length);
            yield return Dwell("townAfterUnload");
            var absentEnd = npcs.Observe(TargetId);
            int targetPeriod = 5 + TargetId % 9;
            int targetOffset = TargetId % targetPeriod;
            int targetEndTick = npcs.TickNumber;
            int expectedSteps = (targetEndTick + targetOffset) / targetPeriod - (targetEndTick - SteadyTicks + targetOffset) / targetPeriod;
            Require(absentEnd.hp == hit.hp && absentEnd.patrolSteps == absentStart.patrolSteps + expectedSteps && expectedSteps > 0 &&
                absentEnd.intent == (TargetId + absentEnd.patrolSteps) % 8 && currentChunk == -1,
                "Offscreen NPC failed to preserve HP and advance its exact scheduled patrol.");

            yield return Travel(5, "revisitChunk5");
            yield return Dwell("revisited5");
            var rebound = loaded[5];
            Require((rebound.ViewIdFor(TargetId) != combatViewId) == stream && SameNpc(rebound.Presented(TargetId), npcs.Observe(TargetId)) &&
                rebound.Presented(TargetId).hp == hit.hp && rebound.Presented(TargetId).patrolSteps > absentEnd.patrolSteps,
                "Target view did not bind current authoritative state on revisit.");

            sampling = false;
            VerifyRenderedImage();
            report.ticks = npcs.TickNumber;
            report.npcUpdates = npcs.NpcUpdates;
            report.otherNpcUpdates = npcs.OtherNpcUpdates;
            report.finalLoadedChunks = CountScenes();
            Require(report.npcUpdates > 0 && report.otherNpcUpdates > 0 && report.loads == (stream ? 4 : 8) &&
                report.unloads == (stream ? 3 : 0), "Counter totals did not match the streamed route or resident control.");

            WorldSave.Publish(output, wolf);
            report.savedJson = File.ReadAllText(output);
            report.wolfRoundTrip = WorldSave.SameState(wolf, WorldSave.Read(report.savedJson));
            report.inputUnchanged = inputBytes.SequenceEqual(File.ReadAllBytes(input));
            report.invalidCandidatesRejected = RejectSave("{") && RejectSave(report.savedJson.Replace("forest-wolf-v2", "forest-wolf")) &&
                RejectSave(report.savedJson.Replace("\"schemaVersion\":2", "\"schemaVersion\":21"));
            Require(report.wolfRoundTrip && report.inputUnchanged && report.invalidCandidatesRejected && report.savedJson == File.ReadAllText(output),
                "Save validation, round-trip or source protection failed.");
        }

        private IEnumerator Travel(int target, string nextStage)
        {
            SetPhase("transition", nextStage);
            long request = Stopwatch.GetTimestamp();
            int startingChunks = CountScenes();
            int departing = currentChunk;
            interestChunk = target;
            tickLimit += TransitionTicks;
            if (target >= 0 && loaded[target] == null)
                yield return Load(target);

            currentChunk = target;
            var destination = target < 0 ? town : loaded[target].gameObject.scene;
            Require(SceneManager.SetActiveScene(destination), $"Cannot activate destination {target}.");
            if (target >= 0)
            {
                loaded[target].Present(npcs, wolf);
                Vector3 center = LargeForestChunk.Center(target);
                worldCamera.orthographicSize = 16;
                worldCamera.transform.position = center + new Vector3(0, 25, -14.43f);
            }
            else
            {
                worldCamera.orthographicSize = 12;
                worldCamera.transform.position = townCameraPosition;
            }
            double readyMs = (Stopwatch.GetTimestamp() - request) * MsPerTick;
            if (stream && departing >= 0)
                yield return Unload(departing);

            if (target < 0)
            {
                var cleanup = Resources.UnloadUnusedAssets();
                while (!cleanup.isDone)
                    yield return null;
            }

            while (npcs.TickNumber < tickLimit)
                yield return null;
            transitions.Add(new Transition
            {
                stage = stage, target = target, chunksAtStart = startingChunks, chunksAtEnd = CountScenes(), requestToReadyMs = readyMs
            });
            SampleMemory(stage);
        }

        private IEnumerator Dwell(string nextStage)
        {
            SetPhase("steady", nextStage);
            tickLimit += SteadyTicks;
            while (npcs.TickNumber < tickLimit)
                yield return null;
            SaveCheckpoint(nextStage, stream ? (currentChunk < 0 ? 0 : 1) : loaded.Length);
            SampleMemory(nextStage);
        }

        private IEnumerator Load(int index)
        {
            string path = LargeForestChunk.ScenePath(index);
            var operation = SceneManager.LoadSceneAsync(path, LoadSceneMode.Additive);
            Require(operation != null, $"Unity refused load request for chunk {index}.");
            while (!operation.isDone)
                yield return null;

            var scene = SceneManager.GetSceneByPath(path);
            Require(scene.isLoaded, $"Chunk {index} was not loaded.");
            var roots = scene.GetRootGameObjects();
            Require(roots.Length == 1, $"Chunk {index} should have one presentation root.");
            var chunk = roots[0].GetComponent<LargeForestChunk>();
            Require(chunk != null && chunk.Index == index && chunk.ViewCount == NpcPopulation.PerChunk, $"Chunk {index} has invalid NPC bindings.");
            report.geometryObjectsPerChunk = roots[0].GetComponentsInChildren<Transform>(true).Length;
            Require(report.geometryObjectsPerChunk >= 700, "Forest chunk has too little authored content.");
            loaded[index] = chunk;
            report.loads++;
            SampleMemory($"loadedChunk{index}");
        }

        private IEnumerator Unload(int index)
        {
            var previousView = loaded[index];
            var operation = SceneManager.UnloadSceneAsync(previousView.gameObject.scene);
            Require(operation != null, $"Unity refused unload request for chunk {index}.");
            while (!operation.isDone)
                yield return null;
            Require(previousView == null && !SceneManager.GetSceneByPath(LargeForestChunk.ScenePath(index)).isLoaded,
                $"Chunk {index} or its presentation survived unload.");
            loaded[index] = null;
            report.unloads++;
        }

        private void Update()
        {
            long now = Stopwatch.GetTimestamp();
            if (!sampling)
            {
                lastFrameAt = now;
                return;
            }
            frames.Add(new FrameSample { phase = phase, stage = stage, milliseconds = (now - lastFrameAt) * MsPerTick });
            lastFrameAt = now;
            if (npcs.TickNumber < tickLimit)
            {
                npcs.Tick(interestChunk);
                if (interestChunk < 0 && wolf.Hp > 0 && npcs.TickNumber % 12 == 0)
                    wolf = wolf.Patrol(1);
                if (currentChunk >= 0)
                    loaded[currentChunk].Present(npcs, wolf);
            }
            if (frames.Count % 16 == 0)
                SampleMemory(stage);
        }

        private void LateUpdate()
        {
            if (renderTarget == null)
                return;
            worldCamera.Render();
            if (sampling)
                report.renderedFrames++;
        }

        private void VerifyRenderedImage()
        {
            worldCamera.Render();
            var previous = RenderTexture.active;
            var readback = new Texture2D(renderTarget.width, renderTarget.height, TextureFormat.RGB24, false);
            try
            {
                RenderTexture.active = renderTarget;
                readback.ReadPixels(new Rect(0, 0, renderTarget.width, renderTarget.height), 0, 0, false);
                var data = readback.GetPixels32();
                var background = data[0];
                foreach (var pixel in data)
                {
                    if (Math.Abs(pixel.r - background.r) + Math.Abs(pixel.g - background.g) + Math.Abs(pixel.b - background.b) > 9)
                        report.nonBackgroundPixels++;
                }
            }
            finally
            {
                RenderTexture.active = previous;
                Destroy(readback);
            }
            Require(report.nonBackgroundPixels > 10000 && report.renderedFrames > 400,
                "The offscreen D3D11 renderer did not produce the expected forest image.");
        }

        private void SaveCheckpoint(string name, int expectedLoaded)
        {
            int actualLoaded = CountScenes();
            Require(actualLoaded == expectedLoaded, $"{name} expected {expectedLoaded} resident forest chunks, found {actualLoaded}.");
            var active = currentChunk < 0 ? null : loaded[currentChunk];
            checkpoints.Add(new Checkpoint
            {
                stage = name, tick = npcs.TickNumber, loadedChunks = actualLoaded, currentChunk = currentChunk,
                wolfHp = wolf.Hp, wolfQuest = wolf.QuestStage, wolfPatrol = wolf.PatrolSteps, npcDigest = npcs.Digest(),
                boundViews = active == null ? 0 : active.ViewCount, targetViewId = currentChunk == 5 ? active.ViewIdFor(TargetId) : 0,
                npcs = new[] { npcs.Observe(0), npcs.Observe(TargetId), npcs.Observe(NpcPopulation.Total - 1) }
            });
        }

        private void SampleMemory(string name)
        {
            var counters = new WindowsMemoryCounters { size = (uint)Marshal.SizeOf<WindowsMemoryCounters>() };
            if (!K32GetProcessMemoryInfo(GetCurrentProcess(), ref counters, counters.size))
                throw new Win32Exception(Marshal.GetLastWin32Error());
            long privateBytes = (long)counters.privateUsage.ToUInt64();
            long workingSet = (long)counters.workingSet.ToUInt64();
            Require(privateBytes > 0 && workingSet > 0, "Windows returned an empty process memory sample.");
            int count = CountScenes();
            report.peakLoadedChunks = Math.Max(report.peakLoadedChunks, count);
            memory.Add(new MemorySample
            {
                stage = name, tick = npcs.TickNumber, elapsedMs = (Stopwatch.GetTimestamp() - startedAt) * MsPerTick,
                privateBytes = privateBytes, workingSetBytes = workingSet, loadedChunks = count
            });
        }

        private static int CountScenes()
        {
            int count = 0;
            for (int i = 0; i < LargeForestChunk.Count; i++)
            {
                if (SceneManager.GetSceneByPath(LargeForestChunk.ScenePath(i)).isLoaded)
                    count++;
            }
            return count;
        }

        private void SetPhase(string nextPhase, string nextStage)
        {
            phase = nextPhase;
            stage = nextStage;
        }

        private void OnDestroy()
        {
            if (renderTarget != null)
                renderTarget.Release();
        }

        private static bool RejectSave(string json)
        {
            try { WorldSave.Read(json); }
            catch (InvalidDataException) { return true; }
            return false;
        }

        private static bool SameNpc(NpcSnapshot a, NpcSnapshot b) =>
            a.id == b.id && a.hp == b.hp && a.patrolSteps == b.patrolSteps && a.intent == b.intent;

        private static void Require(bool condition, string message)
        {
            if (!condition)
                throw new InvalidOperationException(message);
        }
    }
}
