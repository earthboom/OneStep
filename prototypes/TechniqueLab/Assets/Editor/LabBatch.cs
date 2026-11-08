using System;
using System.IO;
using UnityEngine;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEditor.Build;
using UnityEditor.Build.Reporting;
using TechniqueLab;

public static class LabBatch
{
    static readonly string ScenePath="Assets/TechniqueLab.unity";
    [Serializable] public class CheckReport
    {public string unity,utc;public bool editor,playing;public int failures;public CheckResult[] checks;}
    public static void Checks()
    {
        var checks=LabChecks.Run();int failed=checks.FindAll(x=>!x.passed).Count;
        var data=new CheckReport{unity=Application.unityVersion,utc=DateTime.UtcNow.ToString("o"),editor=Application.isEditor,playing=Application.isPlaying,failures=failed,checks=checks.ToArray()};
        string name=Argument("-labReport","checks.json");
        string dir=Path.GetFullPath(Path.Combine(Application.dataPath,"../Results"));Directory.CreateDirectory(dir);
        File.WriteAllText(Path.Combine(dir,name),JsonUtility.ToJson(data,true));
        foreach(var c in checks)Debug.Log("TECHNIQUE_LAB_CHECK "+c.name+" "+(c.passed?"PASS":"FAIL")+" "+c.detail);
        EditorApplication.Exit(failed==0?0:2);
    }
    public static string Argument(string key,string fallback)
    {var a=Environment.GetCommandLineArgs();for(int i=0;i<a.Length-1;i++)if(a[i]==key)return a[i+1];return fallback;}
    public static void PrepareScene()
    {
        EditorSceneManager.NewScene(NewSceneSetup.EmptyScene,NewSceneMode.Single);
        Directory.CreateDirectory("Assets/TechniqueLabMaterials");
        var shader=Shader.Find("Unlit/Color");if(shader==null)throw new InvalidOperationException("Built-in Unlit/Color unavailable");
        Color[] colors={new Color(.055f,.085f,.13f),new Color(.35f,.44f,.55f),new Color(.15f,.85f,1),new Color(1,.3f,.3f),new Color(.25f,1,.55f),new Color(1,.75f,.15f)};
        var materials=new Material[colors.Length];
        for(int i=0;i<colors.Length;i++)
        {string path="Assets/TechniqueLabMaterials/Color"+i+".mat";materials[i]=AssetDatabase.LoadAssetAtPath<Material>(path);
            if(materials[i]==null){materials[i]=new Material(shader);AssetDatabase.CreateAsset(materials[i],path);}materials[i].color=colors[i];EditorUtility.SetDirty(materials[i]);}
        var camera=new GameObject("Main Camera").AddComponent<Camera>();camera.tag="MainCamera";camera.orthographic=true;camera.orthographicSize=18.5f;
        camera.transform.position=new Vector3(0,40,6);camera.transform.rotation=Quaternion.Euler(90,0,0);camera.clearFlags=CameraClearFlags.SolidColor;camera.backgroundColor=new Color(.025f,.04f,.07f);
        var light=new GameObject("Main Light").AddComponent<Light>();light.type=LightType.Directional;light.transform.rotation=Quaternion.Euler(50,-30,0);light.shadows=LightShadows.None;
        var runner=new GameObject("Technique Lab").AddComponent<LabRunner>();runner.materials=materials;runner.font=Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
        if(runner.font==null)throw new InvalidOperationException("Built-in font unavailable");
        EditorSceneManager.SaveScene(EditorSceneManager.GetActiveScene(),ScenePath);
        EditorBuildSettings.scenes=new[]{new EditorBuildSettingsScene(ScenePath,true)};
        PlayerSettings.companyName="OneStep";PlayerSettings.productName="TechniqueLab";
        PlayerSettings.defaultScreenWidth=1280;PlayerSettings.defaultScreenHeight=720;PlayerSettings.fullScreenMode=FullScreenMode.Windowed;
        PlayerSettings.runInBackground=true;PlayerSettings.SetScriptingBackend(NamedBuildTarget.Standalone,ScriptingImplementation.Mono2x);
        AssetDatabase.SaveAssets();
    }
    public static void Prepare(){PrepareScene();Debug.Log("TECHNIQUE_LAB_PREPARED");EditorApplication.Exit(0);}
    public static void Play()
    {EditorSceneManager.OpenScene(ScenePath);EditorApplication.isPlaying=true;}
    [Serializable] public class BuildInfo{public string result,unity,backend;public int errors;public long bytes;public double seconds;}
    public static void Build()
    {
        PrepareScene();Directory.CreateDirectory("Build");
        var result=BuildPipeline.BuildPlayer(new BuildPlayerOptions{scenes=new[]{ScenePath},locationPathName="Build/TechniqueLab.exe",target=BuildTarget.StandaloneWindows64,options=BuildOptions.None});
        Directory.CreateDirectory("Results");
        File.WriteAllText("Results/build.json",JsonUtility.ToJson(new BuildInfo{result=result.summary.result.ToString(),unity=Application.unityVersion,
            backend=PlayerSettings.GetScriptingBackend(NamedBuildTarget.Standalone).ToString(),errors=result.summary.totalErrors,
            bytes=(long)result.summary.totalSize,seconds=result.summary.totalTime.TotalSeconds},true));
        EditorApplication.Exit(result.summary.result==BuildResult.Succeeded?0:2);
    }
}
