using System;
using System.IO;
using WorldLifecycle;

if (args.Length != 1)
    throw new ArgumentException("Pass the path to legacy-v1.json.");

var legacy = File.ReadAllText(args[0]);
var state = WorldSave.Read(legacy);
Require(state.Id == "forest-wolf-v2", "Known legacy ID must resolve to the current catalog ID.");
Require(state.Hp == 100 && state.QuestStage == 0 && state.PatrolSteps == 0,
    "Legacy state must retain all three values.");

var encoded = WorldSave.Write(state);
Require(encoded.Contains("\"schemaVersion\":2"), "Known v1 data must save as schema 2.");
Require(encoded.Contains("\"npcId\":\"forest-wolf-v2\""), "A rewritten slot must use the current catalog ID.");
var reread = WorldSave.Read(encoded);
Require(reread.Hp == 100 && reread.QuestStage == 0 && reread.PatrolSteps == 0, "Current schema must round-trip.");

Reject("{");
Reject("{}");
Reject("{\"schemaVersion\":2,\"npcId\":\"forest-wolf-v2\",\"hp\":0,\"questStage\":0}");
Reject(legacy.Replace("\"schemaVersion\": 1", "\"schemaVersion\": 19"));
Reject(legacy.Replace("\"schemaVersion\": 1", "\"schemaVersion\": 2"));
Reject(legacy.Replace("forest-wolf", "unknown-wolf"));
Reject(legacy.Replace("100", "101"));
var max = WorldSave.Read("{\"schemaVersion\":2,\"npcId\":\"forest-wolf-v2\",\"hp\":3,\"questStage\":1,\"patrolSteps\":2147483647}");
Require(max.Patrol(3).PatrolSteps == int.MaxValue, "The patrol counter must saturate.");
Console.WriteLine("PASS: known legacy data migrates and round-trips; invalid candidates are rejected.");

static void Require(bool condition, string message)
{
    if (!condition)
        throw new InvalidOperationException(message);
}

static void Reject(string candidate)
{
    try
    {
        WorldSave.Read(candidate);
    }
    catch (InvalidDataException)
    {
        return;
    }

    throw new InvalidOperationException($"Accepted an invalid candidate: {candidate}");
}
