using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using UnityEngine;
using Debug=UnityEngine.Debug;
namespace TechniqueLab
{
    [Serializable] public class StreamSample {public int epoch,requested,completed,active,pending,oldestPending;}
    [Serializable] public class StreamBehavior
    {public string name,expectation;public int layout,rate,inflow,epochs,completed,rejected,nativeChecks,nativeHits,nativeMappingErrors,nativeInteriorChecks,nativeTerminalChecks,atInflowCompleted,atInflowPending,maxActive,maxPending;public bool passed,deadlineMet,fifo,stress,negative;public StreamAudit audit;
        public List<StreamJob> jobs;public List<StreamSample> samples=new List<StreamSample>();}
    [Serializable] public class StreamFrame
    {public int frame,steps,epochs,active,renderedActive,visible,pending,requested,completed,oldestPending;public double wallIntervalMs,updateMs,planningMs,backlogSeconds;}
    [Serializable] public class StreamCase
    {public string name;public int rate,layout,minimumActive=256,maximumActive,minimumVisible=256,inflowStart,inflowEnd,completionStart,completionEnd,gen0,gen1,gen2;public double measuredSeconds,maximumBacklog;
        public List<StreamFrame> frames=new List<StreamFrame>(16384);public List<EngineFrame> engineFrames=new List<EngineFrame>(16384);public List<StreamJob> jobs;}
    [Serializable] public class StreamReport
    {public int schemaVersion=1,failures,screenWidth,screenHeight,vSync,antiAliasing;public string utc,unity,buildGuid,cpu,gpu,os,graphicsApi,phase,mode;public bool finished,editor,batch,frameTimingEnabled;public ulong cpuTimerFrequency;
        public CheckResult[] checks;public List<StreamBehavior> behavior=new List<StreamBehavior>();public List<StreamCase> cases=new List<StreamCase>();
        public string scope="Undirected unlaned cardinal grid, static obstacles, fixed .20/.35/.60 discs, FIFO external admission, complete immutable space-time routes and despawning at exits. Finite sustained streams; no experimental proof about infinite time.";}
    public sealed class StreamRunner:MonoBehaviour
    {
        public Material[] materials;public StreamView view;public StreamReport report;string path;bool automated,freeze;double accumulator,phase;
        readonly FrameTiming[] timings=new FrameTiming[1];const double Tick=1.0/60;
        void Error(string text,string stack,LogType type){if(type==LogType.Error||type==LogType.Exception){report.failures++;File.WriteAllText(path+".error.txt",text+"\n"+stack);}}
        IEnumerator Start()
        {
            automated=Application.isBatchMode||Array.IndexOf(Environment.GetCommandLineArgs(),"-streamRun")>=0;
            Application.runInBackground=true;QualitySettings.vSyncCount=0;Application.targetFrameRate=60;
            path=Path.GetFullPath(Path.Combine(Application.dataPath,Application.isEditor?"../Results/Stream":"../../Results/Stream",LabRunner.Argument("-labReport","stream-ui.json")));Directory.CreateDirectory(Path.GetDirectoryName(path));
            report=new StreamReport{utc=DateTime.UtcNow.ToString("o"),unity=Application.unityVersion,buildGuid=Application.buildGUID,cpu=SystemInfo.processorType,gpu=SystemInfo.graphicsDeviceName,os=SystemInfo.operatingSystem,graphicsApi=SystemInfo.graphicsDeviceType.ToString(),
                mode=Application.isEditor?"Editor PlayMode":"Windows release Mono",editor=Application.isEditor,batch=Application.isBatchMode,screenWidth=Screen.width,screenHeight=Screen.height,vSync=QualitySettings.vSyncCount,antiAliasing=QualitySettings.antiAliasing,frameTimingEnabled=FrameTimingManager.IsFeatureEnabled(),cpuTimerFrequency=FrameTimingManager.GetCpuTimerFrequency()};
            Application.logMessageReceived+=Error;view=gameObject.AddComponent<StreamView>();view.materials=materials;view.displayCamera=Camera.main;
            if(!automated){var interactive=new StreamWorld(0,2,int.MaxValue);interactive.Begin();view.Configure(interactive);report.phase="interactive";yield break;}
            var checks=StreamChecks.Run();checks.AddRange(NativeSensitivity());report.checks=checks.ToArray();report.failures+=checks.FindAll(c=>!c.passed).Count;Save("checks");
            foreach(string name in new[]{"baffles-balanced","rooms-crossing","choke-balanced","baffles-biased","choke-overload","baffles-long","rooms-seed19","unreachable-request","lifo-starvation-control","reservation-disabled-control"}){yield return Behavior(name);Save(name);}
            Application.targetFrameRate=-1;
            int order=LabRunner.Argument("-streamOrder","0")=="1"?1:0;
            foreach(int layout in Application.isEditor?new int[0]:order==0?new[]{0,1}:new[]{1,0})
                foreach(int rate in order==0?new[]{1,2,4}:new[]{4,2,1}){yield return Performance(layout,rate);Save("frames-"+layout+"-"+rate);}
            report.finished=true;Save("finished");Application.logMessageReceived-=Error;Debug.Log("STREAM_FINISHED failures="+report.failures);
            #if UNITY_EDITOR
            UnityEditor.EditorApplication.Exit(report.failures==0?0:2);
            #else
            Application.Quit(report.failures==0?0:2);
            #endif
        }
        static int Oldest(StreamWorld w){return w.pending.Count==0?0:w.epoch-w.pending[0].requested;}
        List<CheckResult> NativeSensitivity()
        {
            var rows=new List<CheckResult>();var w=new StreamWorld(0,0,0);w.Request(w.map.portals[0],w.map.portals[4],.35f);w.Begin();view.Configure(w);w.Finish();w.Begin();view.Sync(.5f);
            Transform body=null;foreach(var t in view.GetComponentsInChildren<Transform>())if(t.name.StartsWith("Request 0 radius")){body=t;break;}
            rows.Add(new CheckResult{name="stream.native-baseline",passed=body!=null&&view.MappingErrors(.5f)==0&&view.NativeWallHits(.5f)==0,detail="actual pooled transform matches interpolated logical pose and radius"});
            if(body==null)return rows;
            var scale=body.localScale;body.localScale=new Vector3(scale.x+.2f,scale.y,scale.z);Physics.SyncTransforms();
            rows.Add(new CheckResult{name="stream.native-scale-sensitivity",passed=view.MappingErrors(.5f)>0,detail="deliberate displayed-radius corruption is detected"});body.localScale=scale;
            body.position=new Vector3(0,.5f,0);Physics.SyncTransforms();
            rows.Add(new CheckResult{name="stream.native-pose-sensitivity",passed=view.MappingErrors(.5f)>0,detail="deliberate displayed-position corruption is detected"});
            rows.Add(new CheckResult{name="stream.native-transform-query",passed=view.NativeWallHits(.5f)>0,detail="wall query reads the actual corrupted displayed transform, not the unchanged logical position"});view.Sync(0);return rows;
        }
        IEnumerator Behavior(string name)
        {
            bool lifo=name.StartsWith("lifo"),unsafeMode=name.StartsWith("reservation-disabled"),stress=name=="choke-overload";
            int layout=name.StartsWith("rooms")||lifo?2:name.StartsWith("choke")?1:0,rate=stress?4:unsafeMode?0:name=="unreachable-request"?1:name=="rooms-seed19"?3:2;
            int inflow=lifo?620:name=="baffles-long"?600:unsafeMode?0:120;
            var w=new StreamWorld(layout,rate,inflow,name=="rooms-seed19"?19:0,lifo,unsafeMode,name.EndsWith("biased"));
            if(unsafeMode){w.Request(14+11*32,16+11*32,.6f);w.Request(16+11*32,14+11*32,.35f);}
            if(name=="unreachable-request")w.Request(1+12*32,10+12*32,.6f);
            w.Begin();view.Configure(w);yield return null;report.phase=name;
            var b=new StreamBehavior{name=name,layout=layout,rate=rate,inflow=inflow,audit=new StreamAudit(),stress=stress,negative=lifo||unsafeMode||stress,
                expectation=stress?"overload response deadline failure with eventual drain":lifo?"individual starvation sensitivity":unsafeMode?"collision sensitivity":"safe drain and 240s response deadline"};report.behavior.Add(b);
            bool captured=false;
            while(w.epoch<inflow+1200)
            {
                bool done=false;
                for(int batch=0;batch<4;batch++)
                {
                    for(int sample=0;sample<=4;sample++)
                    {float fraction=sample*.25f;view.Sync(fraction);b.nativeChecks+=w.active.Count;b.nativeHits+=view.NativeWallHits(fraction);b.nativeMappingErrors+=view.MappingErrors(fraction);
                        if(sample>0&&sample<4)b.nativeInteriorChecks+=w.active.Count;
                        if(sample==4)foreach(var j in w.active)if(j.cursor+1==j.path.Length-1)b.nativeTerminalChecks++;}
                    w.Finish();b.audit.Observe(w.map,w.last);b.audit.Watch(w);
                    if(w.epoch%5==0)b.samples.Add(new StreamSample{epoch=w.epoch,requested=w.jobs.Count,completed=w.completed,active=w.active.Count,pending=w.pending.Count,oldestPending=Oldest(w)});
                    if(w.epoch==inflow){b.atInflowCompleted=w.completed;b.atInflowPending=w.pending.Count;}
                    done=unsafeMode&&b.audit.pairPenetrations>0||lifo&&w.epoch>=inflow||!lifo&&w.epoch>=inflow&&w.active.Count==0&&w.pending.Count==0;
                    if(done)break;w.Begin();
                }
                view.Sync(0);
                if(!captured&&w.epoch>=20){Capture(name+"-active");captured=true;}
                yield return null;if(done)break;
            }
            b.epochs=w.epoch;b.completed=w.completed;b.rejected=w.rejected;b.maxActive=w.maxActive;b.maxPending=w.maxPending;b.jobs=w.jobs;
            int previous=-1;b.fifo=true;foreach(var j in w.jobs)if(j.admitted>=0){b.fifo&=j.admitted>=previous;previous=j.admitted;}
            b.deadlineMet=b.audit.deadlineViolations==0;
            b.passed=b.audit.GeometrySafe&&b.nativeHits==0&&b.nativeMappingErrors==0&&w.completed+w.rejected==w.jobs.Count&&w.active.Count==0&&w.pending.Count==0&&b.fifo&&b.audit.maximumGlobalStall<5&&(stress?!b.deadlineMet:b.deadlineMet)&&b.atInflowCompleted>0;
            if(lifo)b.passed=b.audit.GeometrySafe&&b.nativeHits==0&&b.nativeMappingErrors==0&&b.audit.deadlineViolations>0&&w.jobs[0].admitted<0&&w.completed>50;
            if(unsafeMode)b.passed=b.audit.pairPenetrations>0;
            if(!b.passed)report.failures++;Capture(name+"-end");
        }
        IEnumerator Performance(int layout,int rate)
        {
            var w=new StreamWorld(layout,rate,int.MaxValue);w.Begin();for(int i=0;i<40;i++){w.Finish();w.Begin();}
            view.Configure(w);yield return null;phase=0;double backlog=0,start=Time.realtimeSinceStartupAsDouble,previous=start,measure=0;ulong stamp=0;int g0=0,g1=0,g2=0;
            var c=new StreamCase{name=(layout==0?"baffles":"choke")+"-arrival-"+(rate*2)+"-per-second",rate=rate,layout=layout};report.cases.Add(c);report.phase=c.name;var timer=new Stopwatch();
            while(Time.realtimeSinceStartupAsDouble-start<7)
            {
                yield return null;double now=Time.realtimeSinceStartupAsDouble,dt=now-previous;previous=now;bool recording=now-start>=1;
                if(recording&&measure==0){measure=now;c.inflowStart=w.jobs.Count;c.completionStart=w.completed;g0=GC.CollectionCount(0);g1=GC.CollectionCount(1);g2=GC.CollectionCount(2);}
                int renderedActive=w.active.Count,visibleBefore=view.VisibleCount();int epochs=0,steps=0;double plan=0;timer.Restart();backlog+=dt;
                while(backlog>=Tick&&steps<8){phase+=Tick;if(phase>=.5-1e-9){w.Finish();w.Begin();phase-=.5;epochs++;plan+=w.planningMs;}backlog-=Tick;steps++;}
                view.Sync((float)(phase/.5));timer.Stop();FrameTimingManager.CaptureFrameTimings();uint n=FrameTimingManager.GetLatestTimings(1,timings);
                if(!recording)continue;int active=w.active.Count;c.minimumActive=Math.Min(c.minimumActive,active);c.maximumActive=Math.Max(c.maximumActive,active);c.minimumVisible=Math.Min(c.minimumVisible,visibleBefore);c.maximumBacklog=Math.Max(c.maximumBacklog,backlog);
                c.frames.Add(new StreamFrame{frame=Time.frameCount,steps=steps,epochs=epochs,active=active,renderedActive=renderedActive,visible=visibleBefore,pending=w.pending.Count,requested=w.jobs.Count,completed=w.completed,oldestPending=Oldest(w),wallIntervalMs=dt*1000,updateMs=timer.Elapsed.TotalMilliseconds,planningMs=plan,backlogSeconds=backlog});
                if(n>0&&timings[0].frameStartTimestamp>stamp){var t=timings[0];stamp=t.frameStartTimestamp;c.engineFrames.Add(new EngineFrame{timestamp=stamp,cpuMs=t.cpuFrameTime,mainMs=t.cpuMainThreadFrameTime,renderMs=t.cpuRenderThreadFrameTime,presentWaitMs=t.cpuMainThreadPresentWaitTime,gpuMs=t.gpuFrameTime});}
            }
            c.measuredSeconds=previous-measure;c.inflowEnd=w.jobs.Count;c.completionEnd=w.completed;c.jobs=w.jobs;c.gen0=GC.CollectionCount(0)-g0;c.gen1=GC.CollectionCount(1)-g1;c.gen2=GC.CollectionCount(2)-g2;
            if(c.frames.Count<100||c.minimumActive<=0||c.inflowEnd<=c.inflowStart||c.completionEnd<=c.completionStart){report.failures++;Debug.LogError("STREAM_FRAME_ACCEPTANCE_FAILED "+c.name);}Capture(c.name);
        }
        void Update()
        {
            if(automated||freeze||view==null||view.world==null)return;accumulator+=Time.unscaledDeltaTime;int steps=0;
            while(accumulator>=Tick&&steps<8){phase+=Tick;if(phase>=.5-1e-9){view.world.Finish();view.world.Begin();phase-=.5;}accumulator-=Tick;steps++;}view.Sync((float)(phase/.5));
        }
        void OnGUI()
        {
            if(report==null||view==null||view.world==null)return;var w=view.world;GUI.Box(new Rect(10,10,800,160),"UNLANED / SUSTAINED INFLOW / PER-ID ACCOUNTING");
            GUI.Label(new Rect(24,35,770,26),report.phase+" | requested "+w.jobs.Count+" complete "+w.completed+" active "+w.active.Count+" pending "+w.pending.Count);
            GUI.Label(new Rect(24,61,770,26),"Oldest pending "+(Oldest(w)*.5).ToString("F1")+" s | new full-route planning "+w.planningMs.ToString("F2")+" ms | radii .20/.35/.60");GUI.enabled=!automated;
            if(GUI.Button(new Rect(24,96,150,32),w.sourcePaused?"Resume inflow":"Pause inflow"))w.sourcePaused=!w.sourcePaused;
            if(GUI.Button(new Rect(186,96,150,32),freeze?"Resume motion":"Freeze motion"))freeze=!freeze;
            if(GUI.Button(new Rect(348,96,150,32),"Restart choke")){var fresh=new StreamWorld(1,2,int.MaxValue);fresh.Begin();view.Configure(fresh);accumulator=phase=0;}
            if(GUI.Button(new Rect(510,96,150,32),"Quit"))Application.Quit();GUI.enabled=true;
        }
        void Save(string stage){report.phase=stage;File.WriteAllText(path,JsonUtility.ToJson(report,true));}
        void Capture(string suffix)
        {
            var camera=Camera.main;var texture=new RenderTexture(1280,720,24);var previous=RenderTexture.active;var old=camera.targetTexture;camera.targetTexture=texture;camera.Render();RenderTexture.active=texture;
            var image=new Texture2D(1280,720,TextureFormat.RGB24,false);image.ReadPixels(new Rect(0,0,1280,720),0,0);image.Apply();File.WriteAllBytes(Path.ChangeExtension(path,null)+"-"+suffix+".png",image.EncodeToPNG());
            camera.targetTexture=old;RenderTexture.active=previous;Destroy(image);texture.Release();Destroy(texture);
        }
    }
}
