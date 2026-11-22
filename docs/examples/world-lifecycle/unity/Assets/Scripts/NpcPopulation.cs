using System;

namespace WorldLifecycle
{
    [Serializable]
    internal struct NpcSnapshot
    {
        public int id;
        public int hp;
        public int patrolSteps;
        public int intent;
    }

    internal sealed class NpcPopulation
    {
        public const int ChunkCount = 8;
        public const int PerChunk = 256;
        public const int Total = ChunkCount * PerChunk;
        private const int CoarseInterval = 12;

        private struct Record
        {
            public int hp;
            public int patrolSteps;
            public int lastTick;
        }

        private readonly bool coarse;
        private readonly Record[] npcs = new Record[Total];

        public NpcPopulation(bool coarse)
        {
            this.coarse = coarse;
            for (int id = 0; id < npcs.Length; id++)
                npcs[id].hp = 100;
        }

        public int TickNumber { get; private set; }
        public int NpcUpdates { get; private set; }
        public int OtherNpcUpdates { get; private set; }

        public void Tick(int visibleChunk)
        {
            TickNumber++;
            int firstVisible = visibleChunk * PerChunk;
            int endVisible = firstVisible + PerChunk;
            if (coarse && TickNumber % CoarseInterval != 0)
            {
                for (int id = Math.Max(0, firstVisible); id < endVisible; id++)
                    Update(id);
                return;
            }

            for (int id = 0; id < npcs.Length; id++)
            {
                Update(id);
                if (id < firstVisible || id >= endVisible)
                    OtherNpcUpdates++;
            }
        }

        public void Strike(int id) => npcs[id].hp = Math.Max(0, npcs[id].hp - 35);

        public NpcSnapshot Observe(int id)
        {
            ref var record = ref npcs[id];
            int patrol = record.patrolSteps + DueSteps(id, record.lastTick);
            return new NpcSnapshot { id = id, hp = record.hp, patrolSteps = patrol, intent = (id + patrol) % 8 };
        }

        public uint Digest()
        {
            uint digest = 2166136261;
            for (int id = 0; id < npcs.Length; id++)
            {
                var npc = Observe(id);
                digest = unchecked((digest ^ (uint)npc.id) * 16777619);
                digest = unchecked((digest ^ (uint)npc.hp) * 16777619);
                digest = unchecked((digest ^ (uint)npc.patrolSteps) * 16777619);
                digest = unchecked((digest ^ (uint)npc.intent) * 16777619);
            }
            return digest;
        }

        private void Update(int id)
        {
            ref var record = ref npcs[id];
            record.patrolSteps += DueSteps(id, record.lastTick);
            record.lastTick = TickNumber;
            NpcUpdates++;
        }

        private int DueSteps(int id, int fromTick)
        {
            int period = 5 + id % 9;
            int offset = id % period;
            return (TickNumber + offset) / period - (fromTick + offset) / period;
        }
    }
}
