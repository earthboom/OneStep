using System;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.Build.Reporting;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;
using WorldLifecycle;

public static class WorldLifecycleBuild
{
    private const string Content = "Assets/Generated";
    private const string Town = Content + "/Town.unity";
    private const string Forest = Content + "/Forest.unity";

    [MenuItem("World Lifecycle/Prepare and open Town")]
    public static void Prepare()
    {
        if (EditorApplication.isPlaying)
            throw new InvalidOperationException("Stop Play Mode before preparing the project.");

        Directory.CreateDirectory(Content);
        Directory.CreateDirectory(Content + "/Resources");
        File.Copy("../fixtures/legacy-v1.json", Content + "/Resources/legacy-v1.json", true);
        AssetDatabase.Refresh();
        BuildForest();
        LargeForestBuild.Build();
        BuildTown();

        EditorBuildSettings.scenes = new[]
        {
            new EditorBuildSettingsScene(Town, true),
            new EditorBuildSettingsScene(Forest, true)
        }.Concat(Enumerable.Range(0, LargeForestChunk.Count)
            .Select(i => new EditorBuildSettingsScene(LargeForestChunk.ScenePath(i), true))).ToArray();
        PlayerSettings.productName = "World Lifecycle Unity";
        PlayerSettings.fullScreenMode = FullScreenMode.Windowed;
        PlayerSettings.defaultScreenWidth = 1024;
        PlayerSettings.defaultScreenHeight = 640;
        PlayerSettings.runInBackground = true;
        AssetDatabase.SaveAssets();
    }

    public static void BuildWindows()
    {
        Prepare();
        Directory.CreateDirectory("Build");
        var report = BuildPipeline.BuildPlayer(new BuildPlayerOptions
        {
            scenes = EditorBuildSettings.scenes.Select(scene => scene.path).ToArray(),
            locationPathName = "Build/WorldLifecycle.exe",
            target = BuildTarget.StandaloneWindows64,
            options = BuildOptions.None
        });
        if (report.summary.result != BuildResult.Succeeded)
            throw new InvalidOperationException($"Windows build {report.summary.result}.");

        Debug.Log($"WORLD_LIFECYCLE_BUILD_PASS bytes={report.summary.totalSize}");
    }

    private static void BuildTown()
    {
        var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
        var grass = Material("Town lawn", new Color(0.44f, 0.57f, 0.37f));
        var walls = Material("Sandstone", new Color(0.86f, 0.69f, 0.45f));
        var roofs = Material("Terracotta", new Color(0.54f, 0.20f, 0.13f));
        var trail = Material("Path", new Color(0.57f, 0.39f, 0.24f));

        var town = new GameObject("Town geometry").transform;
        Primitive(town, PrimitiveType.Cube, "Town lawn", new Vector3(0, -0.51f, 0), new Vector3(30, 1, 24), grass);
        Primitive(town, PrimitiveType.Cube, "Road", new Vector3(0, 0, 0), new Vector3(25, 0.05f, 3.6f), trail);
        for (int i = 0; i < 5; i++)
        {
            var house = new Vector3(-9 + 4.5f * i, 1.25f, i % 2 == 0 ? 5 : -5);
            Primitive(town, PrimitiveType.Cube, "House", house, new Vector3(2.8f, 2.5f, 2.4f), walls);
            Primitive(town, PrimitiveType.Sphere, "Roof", house + Vector3.up * 1.43f, new Vector3(3.05f, 1.1f, 2.65f), roofs);
        }

        var camera = new GameObject("World camera", typeof(Camera)).GetComponent<Camera>();
        camera.clearFlags = CameraClearFlags.SolidColor;
        camera.backgroundColor = new Color(0.17f, 0.24f, 0.27f);
        camera.orthographic = true;
        camera.orthographicSize = 12;
        camera.farClipPlane = 60;
        camera.transform.position = new Vector3(0, 16, -9.24f);
        camera.transform.rotation = Quaternion.Euler(60, 0, 0);
        var sun = new GameObject("Sun", typeof(Light)).GetComponent<Light>();
        sun.type = LightType.Directional;
        sun.intensity = 1.2f;
        sun.transform.rotation = Quaternion.Euler(48, -37, 0);
        new GameObject("World lifecycle", typeof(WorldLifecycleGame));
        if (!EditorSceneManager.SaveScene(scene, Town))
            throw new IOException("Cannot save Town scene.");
    }

    private static void BuildForest()
    {
        var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
        var forest = new GameObject("Forest geometry").transform;
        forest.position = new Vector3(WorldLifecycleGame.ForestX, 0, 0);
        var floor = Material("Forest floor", new Color(0.27f, 0.38f, 0.20f));
        var trunk = Material("Bark", new Color(0.21f, 0.12f, 0.06f));
        var leaf = Material("Pine", new Color(0.15f, 0.40f, 0.25f));
        var stone = Material("Granite", new Color(0.41f, 0.44f, 0.43f));
        var clearing = Material("Clearing", new Color(0.55f, 0.49f, 0.26f));
        var wolfMaterial = Material("Wolf coat", new Color(0.76f, 0.79f, 0.79f));

        Primitive(forest, PrimitiveType.Cube, "Forest floor", new Vector3(0, -0.51f, 0), new Vector3(30, 1, 26), floor);
        Primitive(forest, PrimitiveType.Sphere, "Clearing", new Vector3(0, 0, 0), new Vector3(16, 0.06f, 12), clearing);
        var random = new System.Random(410);
        for (int i = 0; i < 144; i++)
        {
            float angle = i * Mathf.PI * 2f / 144f;
            float distance = 8.0f + 5.7f * (float)random.NextDouble();
            float height = 1.8f + 1.7f * (float)random.NextDouble();
            var position = new Vector3(Mathf.Cos(angle) * distance, 0, Mathf.Sin(angle) * distance * 0.83f);
            Primitive(forest, PrimitiveType.Cylinder, "Pine trunk", position + Vector3.up * (height * 0.35f), new Vector3(0.3f, height * 0.35f, 0.3f), trunk);
            Primitive(forest, PrimitiveType.Sphere, "Pine crown", position + Vector3.up * height, new Vector3(1.2f, 1.8f, 1.2f), leaf);
            if (i % 3 == 0)
                Primitive(forest, PrimitiveType.Sphere, "Rock", position * 0.90f + Vector3.up * 0.15f, new Vector3(0.8f, 0.42f, 0.7f), stone);
        }

        var wolf = new GameObject("Wolf view", typeof(WolfView)).transform;
        wolf.position = forest.position;
        Primitive(wolf, PrimitiveType.Sphere, "Body", new Vector3(0, 0.64f, 0), new Vector3(1.2f, 0.64f, 0.57f), wolfMaterial);
        Primitive(wolf, PrimitiveType.Sphere, "Head", new Vector3(0.52f, 0.8f, 0), new Vector3(0.55f, 0.51f, 0.43f), wolfMaterial);
        Primitive(wolf, PrimitiveType.Cube, "Tail", new Vector3(-0.68f, 0.71f, 0), new Vector3(0.52f, 0.15f, 0.13f), wolfMaterial);
        for (int side = -1; side <= 1; side += 2)
        {
            Primitive(wolf, PrimitiveType.Cube, "Ear", new Vector3(0.5f, 1.08f, side * 0.15f), new Vector3(0.14f, 0.22f, 0.10f), wolfMaterial);
            Primitive(wolf, PrimitiveType.Cube, "Front leg", new Vector3(0.36f, 0.25f, side * 0.17f), new Vector3(0.16f, 0.49f, 0.12f), wolfMaterial);
            Primitive(wolf, PrimitiveType.Cube, "Rear leg", new Vector3(-0.36f, 0.25f, side * 0.17f), new Vector3(0.16f, 0.49f, 0.12f), wolfMaterial);
        }

        if (!EditorSceneManager.SaveScene(scene, Forest))
            throw new IOException("Cannot save Forest scene.");
    }

    internal static Material Material(string name, Color color)
    {
        var path = $"{Content}/{name}.mat";
        var material = AssetDatabase.LoadAssetAtPath<Material>(path);
        if (material == null)
        {
            var shader = Shader.Find("Standard");
            if (shader == null)
                throw new InvalidOperationException("The built-in render pipeline's Standard shader is missing.");
            material = new Material(shader);
            AssetDatabase.CreateAsset(material, path);
        }

        material.color = color;
        material.SetFloat("_Glossiness", 0.1f);
        EditorUtility.SetDirty(material);
        return material;
    }

    internal static Transform Primitive(Transform parent, PrimitiveType type, string name, Vector3 position, Vector3 scale, Material material)
    {
        var gameObject = GameObject.CreatePrimitive(type);
        gameObject.name = name;
        gameObject.transform.SetParent(parent, false);
        gameObject.transform.localPosition = position;
        gameObject.transform.localScale = scale;
        gameObject.GetComponent<MeshRenderer>().sharedMaterial = material;
        UnityEngine.Object.DestroyImmediate(gameObject.GetComponent<Collider>());
        return gameObject.transform;
    }
}
