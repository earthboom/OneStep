using System;
using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEditor.Build;
using UnityEditor.Build.Reporting;
using UnityEngine;
using TechniqueLab;
public static class TrafficBatch
{
    const string Scene="Assets/TrafficLab.unity";
    public static void Checks()
    {
        var checks=TrafficChecks.Run();int failed=checks.FindAll(c=>!c.passed).Count;
        Directory.CreateDirectory("Results/Traffic");
        File.WriteAllText("Results/Traffic/"+LabBatch.Argument("-labReport","checks.json"),JsonUtility.ToJson(new LabBatch.CheckReport{unity=Application.unityVersion,utc=DateTime.UtcNow.ToString("o"),editor=true,playing=Application.isPlaying,failures=failed,checks=checks.ToArray()},true));
        EditorApplication.Exit(failed==0?0:2);
    }
    static void Prepare()
    {
        EditorSceneManager.NewScene(NewSceneSetup.EmptyScene,NewSceneMode.Single);
        var camera=new GameObject("Main Camera").AddComponent<Camera>();camera.tag="MainCamera";camera.orthographic=true;
        camera.transform.position=new Vector3(63.5f,65,19.5f);camera.transform.rotation=Quaternion.Euler(90,0,0);camera.backgroundColor=new Color(.025f,.04f,.07f);camera.clearFlags=CameraClearFlags.SolidColor;
        new GameObject("Light").AddComponent<Light>().type=LightType.Directional;
        var runner=new GameObject("Traffic experiment").AddComponent<TrafficRunner>();runner.materials=new Material[6];
        for(int i=0;i<6;i++){runner.materials[i]=AssetDatabase.LoadAssetAtPath<Material>("Assets/TechniqueLabMaterials/Color"+i+".mat");if(runner.materials[i]==null)throw new InvalidOperationException("Original materials missing");}
        PlayerSettings.productName="TrafficLab";PlayerSettings.companyName="OneStep";PlayerSettings.defaultScreenWidth=1280;PlayerSettings.defaultScreenHeight=720;
        PlayerSettings.fullScreenMode=FullScreenMode.Windowed;PlayerSettings.runInBackground=true;PlayerSettings.enableFrameTimingStats=true;PlayerSettings.SetScriptingBackend(NamedBuildTarget.Standalone,ScriptingImplementation.Mono2x);
        EditorSceneManager.SaveScene(EditorSceneManager.GetActiveScene(),Scene);AssetDatabase.SaveAssets();
    }
    public static void Play(){Prepare();EditorApplication.isPlaying=true;}
    public static void Build()
    {
        Prepare();Directory.CreateDirectory("TrafficBuild");Directory.CreateDirectory("Results/Traffic");
        var build=BuildPipeline.BuildPlayer(new BuildPlayerOptions{scenes=new[]{Scene},target=BuildTarget.StandaloneWindows64,locationPathName="TrafficBuild/TrafficLab.exe",options=BuildOptions.None});
        File.WriteAllText("Results/Traffic/build.json",JsonUtility.ToJson(new DynamicBatch.BuildRecord{unity=Application.unityVersion,backend="Mono2x",result=build.summary.result.ToString(),
            errors=build.summary.totalErrors,development=false,frameTiming=PlayerSettings.enableFrameTimingStats,seconds=build.summary.totalTime.TotalSeconds,bytes=(long)build.summary.totalSize},true));
        EditorApplication.Exit(build.summary.result==BuildResult.Succeeded?0:2);
    }
}
