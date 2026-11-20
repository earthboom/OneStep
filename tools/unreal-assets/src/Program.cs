using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using OneStep.UnrealAssets;

try
{
    var options = Options.Parse(args);
    if (options.Help)
    {
        Console.WriteLine(Options.Usage);
        return 0;
    }
    var report = AssetReader.Read(options);
    Console.WriteLine(report.ToString(options.Pretty ? Formatting.Indented : Formatting.None));
    return report.Value<string>("status") == "partial" ? 1 : 0;
}
catch (Exception exception)
{
    // CLI boundary: parsing a file is fallible; never turn an exception into an empty asset.
    var code = exception is ReaderException failure ? failure.Code : "parse_failed";
    Console.WriteLine(new JObject
    {
        ["schema_version"] = 1,
        ["status"] = "error",
        ["error"] = new JObject { ["code"] = code, ["message"] = exception.Message }
    }.ToString(Formatting.None));
    return 2;
}
