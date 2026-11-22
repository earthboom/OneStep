using UnityEngine;

namespace WorldLifecycle
{
    public sealed class LargeForestChunk : MonoBehaviour
    {
        public const int Count = NpcPopulation.ChunkCount;
        public const int NpcsPerChunk = NpcPopulation.PerChunk;
        public static string ScenePath(int index) => $"Assets/Generated/LargeForest/Chunk-{index}.unity";
        public static Vector3 Center(int index) => new Vector3(84 + (index % 4) * 55, 0, index / 4 * 55);

        [SerializeField] private int index;
        [SerializeField] private Transform[] npcs;
        [SerializeField] private Transform wolf;
        private readonly NpcSnapshot[] presented = new NpcSnapshot[NpcsPerChunk];

        public void Configure(int chunkIndex, Transform[] npcViews, Transform wolfView)
        {
            index = chunkIndex;
            npcs = npcViews;
            wolf = wolfView;
        }

        internal int Index => index;
        internal int ViewCount => npcs.Length;
        internal int ViewIdFor(int id) => npcs[id % NpcsPerChunk].GetInstanceID();
        internal NpcSnapshot Presented(int id) => presented[id % NpcsPerChunk];

        internal void Present(NpcPopulation population, WolfState state)
        {
            for (int i = 0; i < npcs.Length; i++)
            {
                var npc = population.Observe(index * NpcsPerChunk + i);
                var view = npcs[i];
                if (presented[i].hp == npc.hp && presented[i].patrolSteps == npc.patrolSteps)
                    continue;

                float angle = npc.intent * Mathf.PI / 4;
                view.localPosition = new Vector3((i % 16 - 7.5f) * 1.5f + Mathf.Cos(angle) * .53f,
                    .76f, (i / 16 - 7.5f) * 1.5f + Mathf.Sin(angle) * .53f);
                view.localRotation = Quaternion.Euler(0, npc.intent * 45, npc.hp == 0 ? 90 : npc.hp < 100 ? -18 : 0);
                presented[i] = npc;
            }

            if (index == 5)
            {
                float angle = (state.PatrolSteps % 8) * Mathf.PI / 4;
                wolf.localPosition = new Vector3(Mathf.Cos(angle) * 4.2f, .64f, Mathf.Sin(angle) * 4.2f);
                wolf.localRotation = Quaternion.Euler(0, state.PatrolSteps % 8 * 45, state.Hp == 0 ? 90 : 0);
            }
        }
    }
}
