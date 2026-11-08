using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEditor.Build;
using UnityEditor.Build.Reporting;
using UnityEngine;
using TechniqueLab;
public static class StreamBatch
{
    public static void Checks()
    {
        var checks=StreamChecks.Run();int failed=checks.FindAll(c=>!c.passed).Count;
        Directory.CreateDirectory("Results/Stream");
        File.WriteAllText("Results/Stream/"+LabBatch.Argument("-labReport","checks.json"),JsonUtility.ToJson(new LabBatch.CheckReport{unity=Application.unityVersion,utc=System.DateTime.UtcNow.ToString("o"),editor=true,playing=Application.isPlaying,failures=failed,checks=checks.ToArray()},true));
        EditorApplication.Exit(failed==0?0:2);
    }
    static void Prepare()
    {
        EditorSceneManager.NewScene(NewSceneSetup.EmptyScene,NewSceneMode.Single);
        var camera=new GameObject("Main Camera").AddComponent<Camera>();camera.tag="MainCamera";camera.orthographic=true;camera.orthographicSize=28;
        camera.transform.position=new Vector3(23.25f,65,17.25f);camera.transform.rotation=Quaternion.Euler(90,0,0);camera.backgroundColor=new Color(.025f,.04f,.07f);camera.clearFlags=CameraClearFlags.SolidColor;
        new GameObject("Light").AddComponent<Light>().type=LightType.Directional;
        var runner=new GameObject("Stream experiment").AddComponent<StreamRunner>();runner.materials=new Material[6];
        for(int i=0;i<6;i++){runner.materials[i]=AssetDatabase.LoadAssetAtPath<Material>("Assets/TechniqueLabMaterials/Color"+i+".mat");if(runner.materials[i]==null)throw new System.InvalidOperationException("Original materials missing");}
        PlayerSettings.productName="StreamLab";PlayerSettings.companyName="OneStep";PlayerSettings.defaultScreenWidth=1280;PlayerSettings.defaultScreenHeight=720;PlayerSettings.fullScreenMode=FullScreenMode.Windowed;PlayerSettings.runInBackground=true;PlayerSettings.enableFrameTimingStats=true;PlayerSettings.SetScriptingBackend(NamedBuildTarget.Standalone,ScriptingImplementation.Mono2x);
        EditorSceneManager.SaveScene(EditorSceneManager.GetActiveScene(),"Assets/StreamLab.unity");AssetDatabase.SaveAssets();
    }
    public static void Play(){Prepare();EditorApplication.isPlaying=true;}
    public static void Build()
    {
        Prepare();Directory.CreateDirectory("StreamBuild");Directory.CreateDirectory("Results/Stream");
        var sources=new System.Collections.Generic.List<SourceIdentity>();
        foreach(string file in Directory.GetFiles("Assets","*.cs",SearchOption.AllDirectories))
        {using(var hash=System.Security.Cryptography.SHA256.Create())sources.Add(new SourceIdentity{path=file.Replace('\\','/'),sha256=System.BitConverter.ToString(hash.ComputeHash(File.ReadAllBytes(file))).Replace("-","")});}
        File.WriteAllText("Results/Stream/build-source.json",JsonUtility.ToJson(new SourceSnapshot{utc=System.DateTime.UtcNow.ToString("o"),sources=sources.ToArray()},true));
        var build=BuildPipeline.BuildPlayer(new BuildPlayerOptions{scenes=new[]{"Assets/StreamLab.unity"},target=BuildTarget.StandaloneWindows64,locationPathName="StreamBuild/StreamLab.exe",options=BuildOptions.None});
        File.WriteAllText("Results/Stream/build.json",JsonUtility.ToJson(new DynamicBatch.BuildRecord{unity=Application.unityVersion,backend="Mono2x",result=build.summary.result.ToString(),errors=build.summary.totalErrors,development=false,frameTiming=PlayerSettings.enableFrameTimingStats,seconds=build.summary.totalTime.TotalSeconds,bytes=(long)build.summary.totalSize},true));
        EditorApplication.Exit(build.summary.result==BuildResult.Succeeded?0:2);
    }
    [System.Serializable] public class SourceIdentity {public string path,sha256;}
    [System.Serializable] public class SourceSnapshot {public string utc;public SourceIdentity[] sources;}
}
