using System;
using System.IO;
using UnityEngine;
using UnityEditor;

public static class LabProbe
{
    [Serializable] public class Info
    {
        public string unity, os, cpu, gpu, graphicsApi;
        public int logicalProcessors, memoryMB, graphicsMemoryMB;
        public bool editor, batch, playing;
    }

    public static void Run()
    {
        var data = new Info {
            unity = Application.unityVersion, os = SystemInfo.operatingSystem,
            cpu = SystemInfo.processorType, gpu = SystemInfo.graphicsDeviceName,
            graphicsApi = SystemInfo.graphicsDeviceType.ToString(),
            logicalProcessors = SystemInfo.processorCount, memoryMB = SystemInfo.systemMemorySize,
            graphicsMemoryMB = SystemInfo.graphicsMemorySize,
            editor = Application.isEditor, batch = Application.isBatchMode, playing = Application.isPlaying
        };
        string directory = Path.GetFullPath(Path.Combine(Application.dataPath, "../Results"));
        Directory.CreateDirectory(directory);
        File.WriteAllText(Path.Combine(directory, "engine-probe.json"), JsonUtility.ToJson(data, true));
        Debug.Log("TECHNIQUE_LAB_PROBE " + JsonUtility.ToJson(data));
    }
}
