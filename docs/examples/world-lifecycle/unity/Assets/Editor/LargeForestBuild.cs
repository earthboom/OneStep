using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using WorldLifecycle;
using static WorldLifecycleBuild;

internal static class LargeForestBuild
{
    private const string Content = "Assets/Generated/LargeForest";

    public static void Build()
    {
        Directory.CreateDirectory(Content);
        AssetDatabase.Refresh();
        var bark = Material("Scale bark", new Color(.32f, .21f, .13f));
        var pine = Material("Scale pine", new Color(.24f, .50f, .30f));
        var stone = Material("Scale stone", new Color(.48f, .52f, .49f));
        var npcMat = Material("Scale patrols", new Color(.72f, .43f, .30f));
        var targetMat = Material("Scale scout", new Color(.85f, .62f, .20f));
        var wolfMat = Material("Scale wolf", new Color(.77f, .82f, .83f));
        for (int chunk = 0; chunk < LargeForestChunk.Count; chunk++)
        {
            var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            var root = new GameObject($"Forest chunk {chunk}", typeof(LargeForestChunk)).transform;
            root.position = LargeForestChunk.Center(chunk);
            AddTerrain(root, chunk);

            var random = new System.Random(1769 + chunk);
            for (int i = 0; i < 176; i++)
            {
                float angle = i * Mathf.PI * 2 / 176;
                float radius = 10 + 15 * (float)random.NextDouble();
                float height = 2 + 3 * (float)random.NextDouble();
                var position = new Vector3(radius * Mathf.Cos(angle), 0, radius * Mathf.Sin(angle));
                Primitive(root, PrimitiveType.Cylinder, "Pine trunk", position + Vector3.up * (height * .34f), new Vector3(.4f, height * .42f, .4f), bark);
                Primitive(root, PrimitiveType.Sphere, "Pine canopy", position + Vector3.up * height, new Vector3(2, 3, 2), pine);
                if (i % 2 == 0)
                    Primitive(root, PrimitiveType.Sphere, "Rock", position * .85f + Vector3.up * .23f, new Vector3(1.5f, .5f, .9f), stone);
            }

            var npcs = new Transform[LargeForestChunk.NpcsPerChunk];
            for (int i = 0; i < npcs.Length; i++)
            {
                int id = chunk * npcs.Length + i;
                var color = i == 17 && chunk == 5 ? targetMat : npcMat;
                npcs[i] = Primitive(root, PrimitiveType.Capsule, $"Patrol {id:D4}", Vector3.zero, new Vector3(.47f, .66f, .47f), color);
            }

            var wolf = Primitive(root, PrimitiveType.Sphere, "Wolf view", new Vector3(0, .66f, 0), new Vector3(1.4f, .72f, .69f), wolfMat);
            var head = Primitive(wolf, PrimitiveType.Sphere, "Head", new Vector3(.49f, .32f, 0), new Vector3(.54f, .78f, .65f), wolfMat);
            head.localRotation = Quaternion.Euler(0, 0, -15);
            wolf.gameObject.SetActive(chunk == 5);
            root.GetComponent<LargeForestChunk>().Configure(chunk, npcs, wolf);
            if (!EditorSceneManager.SaveScene(scene, LargeForestChunk.ScenePath(chunk)))
                throw new IOException($"Cannot save forest chunk {chunk}.");
        }
    }

    private static void AddTerrain(Transform root, int chunk)
    {
        const int grid = 72;
        var vertices = new Vector3[(grid + 1) * (grid + 1)];
        var uv = new Vector2[vertices.Length];
        var indices = new int[grid * grid * 6];
        for (int z = 0; z <= grid; z++)
        for (int x = 0; x <= grid; x++)
        {
            int index = z * (grid + 1) + x;
            float u = x / (float)grid;
            float v = z / (float)grid;
            float px = (u - .5f) * 52;
            float pz = (v - .5f) * 52;
            float hill = Mathf.PerlinNoise(u * 6 + chunk * 3, v * 6 + 1) * Mathf.Min(1, (px * px + pz * pz) / 720);
            vertices[index] = new Vector3(px, hill - .25f, pz);
            uv[index] = new Vector2(u, v);
            if (x == grid || z == grid)
                continue;
            int triangle = (z * grid + x) * 6;
            int above = index + grid + 1;
            indices[triangle] = index;
            indices[triangle + 1] = above;
            indices[triangle + 2] = index + 1;
            indices[triangle + 3] = index + 1;
            indices[triangle + 4] = above;
            indices[triangle + 5] = above + 1;
        }

        var meshPath = $"{Content}/Terrain-{chunk}.asset";
        var mesh = AssetDatabase.LoadAssetAtPath<Mesh>(meshPath);
        bool create = mesh == null;
        if (create)
            mesh = new Mesh { name = $"Terrain {chunk}" };
        mesh.Clear();
        mesh.vertices = vertices;
        mesh.uv = uv;
        mesh.triangles = indices;
        mesh.RecalculateNormals();
        if (create)
            AssetDatabase.CreateAsset(mesh, meshPath);
        EditorUtility.SetDirty(mesh);

        var terrain = new GameObject("Textured forest floor", typeof(MeshFilter), typeof(MeshRenderer));
        terrain.transform.SetParent(root, false);
        terrain.GetComponent<MeshFilter>().sharedMesh = mesh;
        var material = Material($"Scale forest floor {chunk}", Color.white);
        material.mainTexture = MakeTerrainTexture(chunk);
        EditorUtility.SetDirty(material);
        terrain.GetComponent<MeshRenderer>().sharedMaterial = material;
    }

    private static Texture2D MakeTerrainTexture(int chunk)
    {
        var path = $"{Content}/Terrain-{chunk}.png";
        var existing = AssetDatabase.LoadAssetAtPath<Texture2D>(path);
        if (existing != null)
            return existing;

        const int size = 1024;
        var pixels = new Color32[size * size];
        for (int y = 0; y < size; y++)
        for (int x = 0; x < size; x++)
        {
            float grain = Mathf.PerlinNoise(x * .05f + chunk * 8, y * .05f) * .3f;
            float patch = Mathf.PerlinNoise(x * .009f, y * .009f + chunk * 11);
            bool pathCorner = Mathf.Abs(x - (size * .50f + 120 * Mathf.Sin(y * .003f + chunk))) < 36;
            var ground = pathCorner ? new Color(.58f, .49f, .31f) : Color.Lerp(new Color(.26f, .34f, .19f), new Color(.47f, .55f, .27f), patch);
            pixels[y * size + x] = ground * (.77f + grain);
        }

        var texture = new Texture2D(size, size, TextureFormat.RGB24, false);
        texture.SetPixels32(pixels);
        texture.Apply();
        File.WriteAllBytes(path, texture.EncodeToPNG());
        Object.DestroyImmediate(texture);
        AssetDatabase.ImportAsset(path, ImportAssetOptions.ForceSynchronousImport);
        return AssetDatabase.LoadAssetAtPath<Texture2D>(path);
    }
}
