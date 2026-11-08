using System;
using System.IO;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using UnityEngine;
using Debug=UnityEngine.Debug;

namespace TechniqueLab
{
    [Serializable] public class FrameResponse
    {public int requestedFPS,frames;public float integratedSeconds,measuredFPS,naiveFinal,exponentialFinal,expected,absoluteError;public float[] deltaSeconds;}
    [Serializable] public class BenchSeries
    {
        public string name,group;public int workPerInvocation,invocationsPerSample,warmupBatches,samples;
        public long totalWorkPerSample,queriesPerSample,stopwatchFrequency;
        public double medianMsPerInvocation,p95MsPerInvocation,checksum,targetTimedBatchMs;
        public double[] rawTimedBatchMs,normalizedMsPerInvocation;
        public int groupGen0Collections,groupGen1Collections,groupGen2Collections;
    }
    [Serializable] public class RunReport
    {
        public string utc,unity,os,cpu,gpu,graphicsApi,buildGuid,mode,phase;
        public int schemaVersion=2,processors,memoryMB,graphicsMemoryMB,failures,frameCount;
        public bool editor,playing,batch,finished;
        public string timingScope="CPU batch operations; scene setup, I/O and rendering outside stopwatch; not total frame/GPU timing. No separate allocation profiler.";
        public CheckResult[] checks;
        public List<FrameResponse> frameResponses=new List<FrameResponse>();
        public List<BenchSeries> benchmarks=new List<BenchSeries>();
    }
    public sealed class LabRunner:MonoBehaviour
    {
        public Material[] materials;public Font font;
        public RunReport report;public LabView view;
        string reportPath,session;bool auto;double sink;
        public static string Argument(string key,string fallback)
        {var a=Environment.GetCommandLineArgs();for(int i=0;i<a.Length-1;i++)if(a[i]==key)return a[i+1];return fallback;}
        IEnumerator Start()
        {
            Application.runInBackground=true;QualitySettings.vSyncCount=0;
            session=Argument("-labReport",Application.isEditor?"editor-play.json":"interactive.json");
            reportPath=Path.GetFullPath(Path.Combine(Application.dataPath,Application.isEditor?"../Results":"../../Results",session));
            Directory.CreateDirectory(Path.GetDirectoryName(reportPath));
            auto=Array.IndexOf(Environment.GetCommandLineArgs(),"-labRun")>=0;
            report=new RunReport{utc=DateTime.UtcNow.ToString("o"),unity=Application.unityVersion,os=SystemInfo.operatingSystem,cpu=SystemInfo.processorType,
                gpu=SystemInfo.graphicsDeviceName,graphicsApi=SystemInfo.graphicsDeviceType.ToString(),processors=SystemInfo.processorCount,
                memoryMB=SystemInfo.systemMemorySize,graphicsMemoryMB=SystemInfo.graphicsMemorySize,buildGuid=Application.buildGUID,
                mode=Application.isEditor?"Editor PlayMode":"Windows standalone",editor=Application.isEditor,playing=Application.isPlaying,batch=Application.isBatchMode,phase="initializing"};
            Application.logMessageReceived+=OnLog;
            view=gameObject.AddComponent<LabView>();view.materials=materials;view.font=font;view.displayCamera=Camera.main;view.Build();
            Application.targetFrameRate=60;
            if(!auto){report.phase="interactive";yield break;}
            yield return null;
            bool injected=Array.IndexOf(Environment.GetCommandLineArgs(),"-labInjectError")>=0;
            if(injected)Debug.LogError("TECHNIQUE_LAB_INJECTED_RUNTIME_ERROR");
            var checks=LabChecks.Run();
            void Add(string name,bool pass,string detail){checks.Add(new CheckResult{name=name,passed=pass,detail=detail});}
            view.SetCover(0);Add("consumer.closed-cover",view.cameraOnlyHit&&view.nativeShot.blocked&&!view.nativeShot.hitTarget,"actual scene consumer reproduces and prevents cover bypass");
            view.CycleCover();Add("consumer.open-cover",view.nativeShot.hitTarget&&!view.nativeShot.blocked,"public cover control reaches open hit");
            view.CycleCover();Add("consumer.inside-cover",view.nativeShot.blocked&&!view.nativeShot.hitTarget,"public cover control reaches origin-overlap rejection");view.SetCover(0);
            view.ToggleDoor();Add("consumer.door-closed",view.field.IsValidFor(view.graph)&&float.IsPositiveInfinity(view.field.distance[0]),"public door control rebuilds unreachable state");
            view.ToggleDoor();Add("consumer.door-open",view.field.IsValidFor(view.graph)&&!float.IsInfinity(view.field.distance[0]),"public door control restores route");
            report.checks=checks.ToArray();report.failures+=checks.FindAll(c=>!c.passed).Count;Save("frame-response");
            if(injected)
            {
                report.finished=true;Save("injected-error-check");
                #if UNITY_EDITOR
                UnityEditor.EditorApplication.Exit(report.failures==0?0:2);
                #else
                Application.Quit(report.failures==0?0:2);
                #endif
                yield break;
            }
            foreach(int cap in new[]{30,60,144})
            {
                Application.targetFrameRate=cap;for(int i=0;i<20;i++)yield return null;
                float elapsed=0,naive=0,correct=0;var deltas=new List<float>();double start=Time.realtimeSinceStartupAsDouble;
                while(elapsed<2f)
                {
                    yield return null;float dt=Mathf.Min(Time.unscaledDeltaTime,2f-elapsed);elapsed+=dt;deltas.Add(dt);
                    naive=Mathf.LerpUnclamped(naive,10,.1f);correct=CameraDamping.Step(correct,10,4,dt);
                }
                float expected=10*(1-Mathf.Exp(-8));float error=Mathf.Abs(correct-expected);
                report.frameResponses.Add(new FrameResponse{requestedFPS=cap,frames=deltas.Count,integratedSeconds=elapsed,
                    measuredFPS=(float)(deltas.Count/(Time.realtimeSinceStartupAsDouble-start)),naiveFinal=naive,exponentialFinal=correct,
                    expected=expected,absoluteError=error,deltaSeconds=deltas.ToArray()});
                if(error>0.0001f)report.failures++;
                Save("frame-response-"+cap);
            }
            Application.targetFrameRate=-1;
            yield return null;Save("camera-bench");CameraBench();
            yield return null;Save("physics-bench");PhysicsBench();
            yield return null;Save("path-bench");PathBench();
            Application.targetFrameRate=60;view.SetCover(0);
            for(int i=0;i<20;i++)yield return null;
            Save("capture");Capture();
            report.finished=true;report.frameCount=Time.frameCount;Save("finished");
            Debug.Log("TECHNIQUE_LAB_FINISHED "+session+" failures="+report.failures);
            Application.logMessageReceived-=OnLog;
            #if UNITY_EDITOR
            UnityEditor.EditorApplication.Exit(report.failures==0?0:2);
            #else
            Application.Quit(report.failures==0?0:2);
            #endif
        }
        void OnLog(string message,string stack,LogType type)
        {if(type==LogType.Exception||type==LogType.Error){report.failures++;report.phase="runtime-error";File.WriteAllText(reportPath+".error.txt",message+"\n"+stack);}}
        void Save(string phase){report.phase=phase;File.WriteAllText(reportPath,JsonUtility.ToJson(report,true));}
        sealed class Workload {public string name;public Action action;public Workload(string name,Action action){this.name=name;this.action=action;}}
        void Group(string group,int work,params Workload[] cases)
        {
            const int warmup=8,samples=31;const double targetMs=3;var rows=new BenchSeries[cases.Length];var timer=new Stopwatch();
            for(int c=0;c<cases.Length;c++)
            {
                for(int i=0;i<warmup;i++)cases[c].action();
                int repeats=1;
                while(true)
                {
                    timer.Restart();for(int j=0;j<repeats;j++)cases[c].action();timer.Stop();
                    if(timer.Elapsed.TotalMilliseconds>=targetMs||repeats>=1048576)break;
                    repeats*=2;
                }
                rows[c]=new BenchSeries{name=cases[c].name,group=group,workPerInvocation=work,invocationsPerSample=repeats,
                    totalWorkPerSample=(long)work*repeats,warmupBatches=warmup,samples=samples,targetTimedBatchMs=targetMs,
                    stopwatchFrequency=Stopwatch.Frequency,rawTimedBatchMs=new double[samples],normalizedMsPerInvocation=new double[samples]};
            }
            int gc0=GC.CollectionCount(0),gc1=GC.CollectionCount(1),gc2=GC.CollectionCount(2);
            for(int sample=0;sample<samples;sample++)for(int order=0;order<cases.Length;order++)
            {
                int c=sample%2==0?order:cases.Length-1-order;long before=ShotResolver.QueryCount;
                timer.Restart();for(int j=0;j<rows[c].invocationsPerSample;j++)cases[c].action();timer.Stop();
                rows[c].rawTimedBatchMs[sample]=timer.Elapsed.TotalMilliseconds;
                rows[c].normalizedMsPerInvocation[sample]=timer.Elapsed.TotalMilliseconds/rows[c].invocationsPerSample;
                rows[c].queriesPerSample=ShotResolver.QueryCount-before;
                rows[c].checksum=sink;
            }
            foreach(var row in rows)
            {var sorted=(double[])row.normalizedMsPerInvocation.Clone();Array.Sort(sorted);row.medianMsPerInvocation=sorted[samples/2];row.p95MsPerInvocation=sorted[(int)Math.Ceiling(samples*.95)-1];
                row.groupGen0Collections=GC.CollectionCount(0)-gc0;row.groupGen1Collections=GC.CollectionCount(1)-gc1;row.groupGen2Collections=GC.CollectionCount(2)-gc2;report.benchmarks.Add(row);}
        }
        void CameraBench()
        {
            const int count=100000;var a=new float[count];var b=new float[count];var c=new float[count];
            Group("100000 scalar followers, dt=1/60, CPU math only",count,
                new Workload("camera.frame-lerp",()=>{double sum=0;for(int i=0;i<count;i++){a[i]=Mathf.LerpUnclamped(a[i],i%17,.1f);sum+=a[i];}sink=sum;}),
                new Workload("camera.exp-per-item",()=>{double sum=0;for(int i=0;i<count;i++){b[i]=CameraDamping.Step(b[i],i%17,4,1f/60);sum+=b[i];}sink=sum;}),
                new Workload("camera.exp-shared-alpha",()=>{float alpha=CameraDamping.Alpha(4,1f/60);double sum=0;for(int i=0;i<count;i++){c[i]=Mathf.LerpUnclamped(c[i],i%17,alpha);sum+=c[i];}sink=sum;}));
        }
        void PhysicsBench()
        {
            foreach(int state in new[]{0,1,2})foreach(int count in new[]{32,256,1024})
            {
                view.SetCover(state);var camera=view.ShotCamera;var direction=view.ShotDirection;var root=view.WeaponRoot;var muzzle=view.Muzzle;
                Group("native physics cover="+state+", same static query pose",count,
                    new Workload("shot.camera-only",()=>{int hits=0;for(int i=0;i<count;i++)if(ShotResolver.CameraOnly(camera,direction,50).hitTarget)hits++;sink=hits;}),
                    new Workload("shot.intent-muzzle-safe",()=>{int hits=0;for(int i=0;i<count;i++)if(ShotResolver.Resolve(camera,direction,root,muzzle,50).hitTarget)hits++;sink=hits;}));
            }
        }
        void PathBench()
        {
            var graph=WeightedGraph.Grid(32);var field=new WeightedField(graph.Count);var search=new AStarWorkspace(graph.Count);int goal=graph.Count-1;field.Compute(graph,goal);
            foreach(int count in new[]{32,128,512})
            {
                var starts=new int[count];for(int i=0;i<count;i++){starts[i]=(i*31+7)%graph.Count;while(graph.blocked[starts[i]])starts[i]=(starts[i]+1)%graph.Count;}
                Group("32x32 weighted grid, same goal; distance answers only; no steering",count,
                    new Workload("path.independent-astar-distance",()=>{double sum=0;foreach(int start in starts)sum+=search.Cost(graph,start,goal);sink=sum;}),
                    new Workload("path.field-rebuild-plus-distance",()=>{field.Compute(graph,goal);double sum=0;foreach(int start in starts)sum+=field.distance[start];sink=sum;}),
                    new Workload("path.cached-field-distance",()=>{double sum=0;foreach(int start in starts)sum+=field.distance[start];sink=sum;}));
            }
        }
        void Capture()
        {
            var camera=Camera.main;var texture=new RenderTexture(1280,720,24);var previous=RenderTexture.active;var old=camera.targetTexture;
            camera.targetTexture=texture;camera.Render();RenderTexture.active=texture;var image=new Texture2D(1280,720,TextureFormat.RGB24,false);
            image.ReadPixels(new Rect(0,0,1280,720),0,0);image.Apply();File.WriteAllBytes(Path.ChangeExtension(reportPath,"png"),image.EncodeToPNG());
            camera.targetTexture=old;RenderTexture.active=previous;Destroy(image);texture.Release();Destroy(texture);
        }
        void OnGUI()
        {
            if(view==null||report==null)return;
            GUI.Box(new Rect(12,12,440,220),"TECHNIQUE LAB  /  UNITY "+Application.unityVersion);
            GUI.Label(new Rect(28,43,410,26),report.mode+"  |  "+report.phase);
            GUI.enabled=!auto;
            if(GUI.Button(new Rect(28,77,120,30),"Reset followers"))view.ResetCamera();
            if(GUI.Button(new Rect(160,77,120,30),"Cycle cover"))view.CycleCover();
            if(GUI.Button(new Rect(292,77,140,30),"Toggle grid door"))view.ToggleDoor();
            GUI.enabled=true;
            GUI.Label(new Rect(28,120,405,24),"Camera-only target: "+view.cameraOnlyHit+" | safe blocked: "+view.nativeShot.blocked);
            GUI.Label(new Rect(28,148,405,24),"Grid: 64 route consumers | door closed: "+view.DoorClosed);
            GUI.Label(new Rect(28,176,405,24),"Cyan target / red frame lerp / green exponential");
            if(!auto&&GUI.Button(new Rect(28,202,120,22),"Quit"))Application.Quit();
        }
    }
}
