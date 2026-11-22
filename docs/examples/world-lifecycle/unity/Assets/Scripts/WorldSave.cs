using System;
using System.IO;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Json;
using System.Text;

namespace WorldLifecycle
{
    internal sealed class WolfState
    {
        public WolfState(string id, int hp, int questStage, int patrolSteps)
        {
            Id = id;
            Hp = hp;
            QuestStage = questStage;
            PatrolSteps = patrolSteps;
        }

        public string Id { get; }
        public int Hp { get; }
        public int QuestStage { get; }
        public int PatrolSteps { get; }

        public WolfState Hit() => new WolfState(Id, Math.Max(0, Hp - 40), 1, PatrolSteps);
        public WolfState Patrol(int elapsedSteps) =>
            new WolfState(Id, Hp, QuestStage, PatrolSteps + Math.Min(int.MaxValue - PatrolSteps, elapsedSteps));
    }

    internal static class WorldCatalog
    {
        public const string WolfId = "forest-wolf-v2";
    }

    internal static class WorldSave
    {
        private const string LegacyWolfId = "forest-wolf";
        private const int CurrentSchema = 2;

        [DataContract]
        private sealed class SaveRecord
        {
            [DataMember(Name = "schemaVersion", IsRequired = true, Order = 0)] public int Version;
            [DataMember(Name = "npcId", IsRequired = true, Order = 1)] public string Id;
            [DataMember(Name = "hp", IsRequired = true, Order = 2)] public int Hp;
            [DataMember(Name = "questStage", IsRequired = true, Order = 3)] public int QuestStage;
            [DataMember(Name = "patrolSteps", IsRequired = true, Order = 4)] public int PatrolSteps;
        }

        public static WolfState Read(string json)
        {
            SaveRecord record;
            try
            {
                using var stream = new MemoryStream(Encoding.UTF8.GetBytes(json));
                record = (SaveRecord)new DataContractJsonSerializer(typeof(SaveRecord)).ReadObject(stream);
            }
            catch (SerializationException exception)
            {
                throw new InvalidDataException("Malformed world save.", exception);
            }

            if (record == null)
                throw new InvalidDataException("Missing world save record.");
            switch (record.Version)
            {
                case 1 when record.Id == LegacyWolfId:
                case CurrentSchema when record.Id == WorldCatalog.WolfId:
                    break;
                case 1:
                case CurrentSchema:
                    throw new InvalidDataException("Save has an unknown NPC ID for its schema.");
                default:
                    throw new InvalidDataException($"Unsupported schema {record.Version}.");
            }

            if (record.Hp < 0 || record.Hp > 100 || record.QuestStage < 0 || record.QuestStage > 1 || record.PatrolSteps < 0)
                throw new InvalidDataException("Save state is outside its supported range.");

            return new WolfState(WorldCatalog.WolfId, record.Hp, record.QuestStage, record.PatrolSteps);
        }

        public static string Write(WolfState state)
        {
            using var stream = new MemoryStream();
            var record = new SaveRecord
            {
                Version = CurrentSchema,
                Id = state.Id,
                Hp = state.Hp,
                QuestStage = state.QuestStage,
                PatrolSteps = state.PatrolSteps
            };
            new DataContractJsonSerializer(typeof(SaveRecord)).WriteObject(stream, record);
            return Encoding.UTF8.GetString(stream.ToArray());
        }

        public static void Publish(string path, WolfState state)
        {
            var file = Path.GetFullPath(path);
            Directory.CreateDirectory(Path.GetDirectoryName(file));
            var pending = $"{file}.{Guid.NewGuid():N}.pending";
            try
            {
                File.WriteAllText(pending, Write(state));
                var verified = Read(File.ReadAllText(pending));
                if (!SameState(verified, state))
                    throw new InvalidDataException("Save verification did not reproduce the snapshot.");
                if (File.Exists(file))
                    File.Replace(pending, file, null);
                else
                    File.Move(pending, file);
            }
            finally
            {
                if (File.Exists(pending))
                    File.Delete(pending);
            }
        }

        public static bool SameState(WolfState a, WolfState b) =>
            a.Id == b.Id && a.Hp == b.Hp && a.QuestStage == b.QuestStage && a.PatrolSteps == b.PatrolSteps;
    }
}
