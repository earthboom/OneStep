using System;
using System.IO;
using UnityEngine;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEditor.Build;
using UnityEditor.Build.Reporting;
using TechniqueLab;

public static class DynamicBatch
{
    const string Scene="Assets/DynamicLab.unity";
    public static void Checks()
    {
        var list=CrowdChecks.Run();int failures=list.FindAll(x=>!x.passed).Count;
        var report=new LabBatch.CheckReport{unity=Application.unityVersion,utc=DateTime.UtcNow.ToString("o"),editor=true,playing=Application.isPlaying,failures=failures,checks=list.ToArray()};
        Directory.CreateDirectory("Results/Dynamic");
        File.WriteAllText("Results/Dynamic/"+LabBatch.Argument("-labReport","checks.json"),JsonUtility.ToJson(report,true));
        EditorApplication.Exit(failures==0?0:2);
    }
    static void PrepareScene()
    {
        EditorSceneManager.NewScene(NewSceneSetup.EmptyScene,NewSceneMode.Single);
        var camera=new GameObject("Main Camera").AddComponent<Camera>();camera.tag="MainCamera";
        camera.orthographic=true;camera.orthographicSize=15;camera.transform.position=new Vector3(12,65,8);camera.transform.rotation=Quaternion.Euler(90,0,0);
        camera.clearFlags=CameraClearFlags.SolidColor;camera.backgroundColor=new Color(.025f,.04f,.07f);
        new GameObject("Directional Light").AddComponent<Light>().type=LightType.Directional;
        var runner=new GameObject("Dynamic field experiment").AddComponent<DynamicRunner>();runner.materials=new Material[6];
        for(int i=0;i<6;i++)
        {runner.materials[i]=AssetDatabase.LoadAssetAtPath<Material>("Assets/TechniqueLabMaterials/Color"+i+".mat");if(runner.materials[i]==null)throw new InvalidOperationException("Prepare original lab materials first");}
        PlayerSettings.companyName="OneStep";PlayerSettings.productName="DynamicLab";PlayerSettings.defaultScreenWidth=1280;PlayerSettings.defaultScreenHeight=720;
        PlayerSettings.fullScreenMode=FullScreenMode.Windowed;PlayerSettings.runInBackground=true;PlayerSettings.enableFrameTimingStats=true;
        PlayerSettings.SetScriptingBackend(NamedBuildTarget.Standalone,ScriptingImplementation.Mono2x);
        EditorSceneManager.SaveScene(EditorSceneManager.GetActiveScene(),Scene);AssetDatabase.SaveAssets();
    }
    public static void Prepare(){PrepareScene();EditorApplication.Exit(0);}
    public static void Play(){PrepareScene();EditorApplication.isPlaying=true;}
    [Serializable] public class BuildRecord
    {public string unity,backend,result;public int errors;public bool development,frameTiming;public double seconds;public long bytes;}
    public static void Build()
    {
        PrepareScene();Directory.CreateDirectory("DynamicBuild");
        var build=BuildPipeline.BuildPlayer(new BuildPlayerOptions{scenes=new[]{Scene},target=BuildTarget.StandaloneWindows64,
            locationPathName="DynamicBuild/DynamicLab.exe",options=BuildOptions.None});
        Directory.CreateDirectory("Results/Dynamic");
        File.WriteAllText("Results/Dynamic/build.json",JsonUtility.ToJson(new BuildRecord{unity=Application.unityVersion,backend="Mono2x",result=build.summary.result.ToString(),
            errors=build.summary.totalErrors,development=false,frameTiming=PlayerSettings.enableFrameTimingStats,seconds=build.summary.totalTime.TotalSeconds,bytes=(long)build.summary.totalSize},true));
        EditorApplication.Exit(build.summary.result==BuildResult.Succeeded?0:2);
    }
}
