using System;
using System.IO;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using UnityEngine;
using Debug=UnityEngine.Debug;

namespace TechniqueLab
{
    [Serializable] public struct DynamicFrame
    {
        public int frame,steps,active,pending;
        public double wallIntervalMs,updateMs,backlogSeconds;
    }
    [Serializable] public struct EngineFrame
    {
        public ulong timestamp;
        public double cpuMs,mainMs,renderMs,presentWaitMs,gpuMs;
    }
    [Serializable] public class ObstacleEvent
    {
        public string action;public int cell,moving,pending,solid,engineFrame;
        public double simulatedSeconds,milliseconds;
        public float maximumPoseChange;
    }
    [Serializable] public class BehaviorResult
    {
        public string name;public int agents,arrived,ticks,nativeChecks,nativeWallOverlaps,alternateCrossings,width,height,closeRequestTick=-1,closeCommitTick=-1;
        public float simulatedSeconds;public bool triggered,passed,bodyOccupiedAtRequest;
        public CrowdAudit audit;
        public List<ObstacleEvent> events=new List<ObstacleEvent>();
    }
    [Serializable] public class FrameCase
    {
        public string name;public int agents,minimumActive,maximumActive,rebuilds,gen0,gen1,gen2;
        public bool avoidance;public double warmupSeconds=1,measuredSeconds,maximumBacklog;
        public List<DynamicFrame> frames=new List<DynamicFrame>(16384);
        public List<EngineFrame> engineFrames=new List<EngineFrame>(16384);
        public List<ObstacleEvent> events=new List<ObstacleEvent>();
    }
    [Serializable] public class DynamicReport
    {
        public int schemaVersion=1,failures,width,height,logicalProcessors,memoryMB,screenWidth,screenHeight,vSync,antiAliasing;
        public ulong cpuTimerFrequency;
        public string utc,unity,mode,cpu,gpu,graphicsApi,os,buildGuid,phase;
        public bool finished,editor,batch,frameTimingEnabled;
        public CheckResult[] checks;
        public List<BehaviorResult> behavior=new List<BehaviorResult>();
        public List<FrameCase> cases=new List<FrameCase>();
        public string timingScope="Whole rendered frame intervals; Unity FrameTimingManager CPU/GPU when nonzero, asynchronously reported; CPU/GPU overlap and must not be added. 60Hz simulation, no discarded wall deltas. Update component timer includes transactions, movement, transform sync; geometry/native audits disabled in performance. Setup, JSON and captures outside performance windows.";
    }
    public sealed class DynamicRunner:MonoBehaviour
    {
        public Material[] materials;
        public DynamicReport report;
        public DynamicView view;
        const float Tick=1f/60;
        string reportPath;bool automated,paused;double interactiveAccumulator;int crate=-1;
        FrameTiming[] timings=new FrameTiming[1];
        void RecordError(string message,string stack,LogType type)
        {if(type==LogType.Error||type==LogType.Exception){report.failures++;File.WriteAllText(reportPath+".error.txt",message+"\n"+stack);}}
        IEnumerator Start()
        {
            Application.runInBackground=true;QualitySettings.vSyncCount=0;Application.targetFrameRate=60;
            automated=Application.isBatchMode||Array.IndexOf(Environment.GetCommandLineArgs(),"-dynamicRun")>=0;
            string name=LabRunner.Argument("-labReport","dynamic-interactive.json");
            reportPath=Path.GetFullPath(Path.Combine(Application.dataPath,Application.isEditor?"../Results/Dynamic":"../../Results/Dynamic",name));
            Directory.CreateDirectory(Path.GetDirectoryName(reportPath));
            report=new DynamicReport{utc=DateTime.UtcNow.ToString("o"),unity=Application.unityVersion,editor=Application.isEditor,
                mode=Application.isEditor?"Editor PlayMode":"Windows standalone Mono release",cpu=SystemInfo.processorType,gpu=SystemInfo.graphicsDeviceName,
                graphicsApi=SystemInfo.graphicsDeviceType.ToString(),os=SystemInfo.operatingSystem,logicalProcessors=SystemInfo.processorCount,
                memoryMB=SystemInfo.systemMemorySize,buildGuid=Application.buildGUID,phase="initializing",frameTimingEnabled=FrameTimingManager.IsFeatureEnabled(),
                batch=Application.isBatchMode,screenWidth=Screen.width,screenHeight=Screen.height,vSync=QualitySettings.vSyncCount,antiAliasing=QualitySettings.antiAliasing,
                cpuTimerFrequency=FrameTimingManager.GetCpuTimerFrequency()};
            Application.logMessageReceived+=RecordError;
            view=gameObject.AddComponent<DynamicView>();view.materials=materials;view.cameraView=Camera.main;
            if(!automated){view.Configure(Spawn(24,16,32));report.phase="interactive";yield break;}
            var checks=CrowdChecks.Run();report.checks=checks.ToArray();report.failures+=checks.FindAll(c=>!c.passed).Count;Save("behavior");
            foreach(string scenario in new[]{"occupied-door","all-blocked","moving-crate","dense-64","dense-256","avoidance-disabled-control"})
            {yield return Behavior(scenario);Save("behavior-"+scenario);}
            Application.targetFrameRate=-1;
            int variant=LabRunner.Argument("-dynamicOrder","0")=="1"?1:0;
            // Batch Editor PlayMode verifies behavior but does not continuously render a Game view.
            // Whole-frame performance belongs to the actual non-batch graphical player only.
            foreach(int count in Application.isEditor?new int[0]:new[]{64,256,512})for(int order=0;order<2;order++)
            {yield return Performance(count,(order+variant)%2==0);Save("performance-"+count+"-"+order);}
            Application.targetFrameRate=60;view.Configure(Spawn(24,16,32));
            for(int i=0;i<10;i++){view.world.Step(Tick);view.Sync();yield return null;}
            Capture("final");report.finished=true;Save("finished");
            Debug.Log("DYNAMIC_LAB_FINISHED failures="+report.failures);Application.logMessageReceived-=RecordError;
            #if UNITY_EDITOR
            UnityEditor.EditorApplication.Exit(report.failures==0?0:2);
            #else
            Application.Quit(report.failures==0?0:2);
            #endif
        }
        public static CrowdWorld Spawn(int width,int height,int count,bool avoidance=true)
        {
            var w=new CrowdWorld(width,height,count){avoidance=avoidance};int rows=height-4;
            for(int i=0;i<count;i++)w.Place(i,(2+i%rows)*width+2+i/rows);
            return w;
        }
        ObstacleEvent Change(CrowdWorld w,int cell,bool close,string name)
        {
            var before=new Vector2[w.agents.Length];for(int i=0;i<before.Length;i++)before[i]=w.agents[i].position;
            var timer=Stopwatch.StartNew();if(close)w.Close(cell);else w.Open(cell);timer.Stop();
            // Public obstacle controls also work while paused; logical and native/visual state stay aligned.
            if(view!=null&&view.world==w)view.Sync();
            var e=new ObstacleEvent{action=name,cell=cell,milliseconds=timer.Elapsed.TotalMilliseconds,simulatedSeconds=w.ticks*Tick,pending=w.pendingCount,solid=w.closedCount,engineFrame=Time.frameCount};
            for(int i=0;i<before.Length;i++){e.maximumPoseChange=Mathf.Max(e.maximumPoseChange,Vector2.Distance(before[i],w.agents[i].position));if(w.agents[i].next>=0)e.moving++;}
            if(e.maximumPoseChange>0||!w.Fresh)report.failures++;
            return e;
        }
        public void SetObstacle(int cell,bool close){Change(view.world,cell,close,"public obstacle control");}
        public void TogglePause(){paused=!paused;}
        IEnumerator Behavior(string name)
        {
            int count=name=="dense-256"?256:name=="dense-64"?64:name=="occupied-door"?16:32;
            CrowdWorld w;
            if(name=="occupied-door")
            {w=new CrowdWorld(24,16,count);w.Place(0,w.doorA-1);for(int i=1;i<count;i++)w.Place(i,(2+(i-1)%10)*24+2+(i-1)/10);}
            else w=Spawn(name=="dense-256"?48:32,name=="dense-256"?28:24,count,name!="avoidance-disabled-control");
            if(name=="moving-crate")
            {w=new CrowdWorld(24,16,count);w.Place(0,4*24+5);for(int i=1;i<count;i++)w.Place(i,(2+(i-1)%12)*24+2+(i-1)/12);}
            view.Configure(w);yield return null;
            var b=new BehaviorResult{name=name,agents=count,width=w.width,height=w.height,audit=new CrowdAudit(w)};report.behavior.Add(b);bool requested=false,second=false,third=false,safeWait=false;
            int obstacle=-1,watchedObstacle=-1;float limit=name=="dense-256"?120:60;
            if(name=="avoidance-disabled-control")limit=10;
            report.phase="behavior "+name;
            while(w.ticks*Tick<limit&&w.arrived<count)
            {
                for(int batch=0;batch<8&&w.arrived<count&&w.ticks*Tick<limit;batch++)
                {
                    float time=w.ticks*Tick;
                    if(name=="occupied-door"&&!requested&&w.agents[0].next==w.doorA&&Vector2.Distance(w.agents[0].position,w.Center(w.doorA-1))>.75f)
                    {var relative=w.agents[0].position-w.Center(w.doorA);b.bodyOccupiedAtRequest=Mathf.Abs(relative.x)+CrowdWorld.Radius<.5f&&Mathf.Abs(relative.y)+CrowdWorld.Radius<.5f;
                        b.events.Add(Change(w,w.doorA,true,"close-occupied-door"));requested=true;b.triggered=w.Pending(w.doorA);b.closeRequestTick=w.ticks;watchedObstacle=w.doorA;view.Sync();Capture(name+"-pending");}
                    if(name=="all-blocked")
                    {
                        if(!requested&&time>=2){b.events.Add(Change(w,w.doorA,true,"close-main"));b.events.Add(Change(w,w.doorB,true,"close-alternate"));requested=true;}
                        if(requested&&!second&&time>=6)
                        {safeWait=true;foreach(var a in w.agents)if(!a.arrived&&a.next>=0)safeWait=false;b.triggered=safeWait&&w.pendingCount==0;
                            b.events.Add(Change(w,w.doorA,false,"reopen-main"));second=true;}
                    }
                    if(name=="moving-crate")
                    {
                        if(!requested&&w.agents[0].next>=0&&Vector2.Distance(w.agents[0].position,w.Center(w.agents[0].cell))>.1f)
                        {obstacle=w.agents[0].next;b.events.Add(Change(w,obstacle,true,"crate-occupied-request"));b.triggered=w.Pending(obstacle);b.closeRequestTick=w.ticks;watchedObstacle=obstacle;requested=true;}
                        if(requested&&!second&&time>=2){b.events.Add(Change(w,obstacle,false,"crate-remove-1"));obstacle=4*24+8;b.events.Add(Change(w,obstacle,true,"crate-place-2"));second=true;}
                        if(second&&!third&&time>=4){b.events.Add(Change(w,obstacle,false,"crate-remove-2"));obstacle=4*24+9;b.events.Add(Change(w,obstacle,true,"crate-place-3"));third=true;}
                    }
                    w.Step(Tick);b.audit.Observe(w,Tick);
                    if(watchedObstacle>=0&&b.closeCommitTick<0&&w.Solid(watchedObstacle))b.closeCommitTick=w.ticks;
                }
                view.Sync();b.nativeWallOverlaps+=view.NativeWallOverlaps();b.nativeChecks+=w.agents.Length-w.arrived;
                yield return null;
            }
            b.arrived=w.arrived;b.ticks=w.ticks;b.simulatedSeconds=w.ticks*Tick;b.alternateCrossings=w.alternateCrossings;
            bool expectation=name=="avoidance-disabled-control"?b.audit.pairPenetrations>0:
                b.audit.Safe&&b.nativeWallOverlaps==0&&w.arrived==count;
            if(name=="occupied-door")expectation&=b.triggered&&b.bodyOccupiedAtRequest&&w.Solid(w.doorA)&&w.alternateCrossings>0&&b.closeCommitTick>=b.closeRequestTick&&(b.closeCommitTick-b.closeRequestTick)*Tick<=2;
            if(name=="all-blocked")expectation&=b.triggered&&second;
            if(name=="moving-crate")expectation&=b.triggered&&third;
            b.passed=expectation;if(!expectation)report.failures++;
            Capture(name+"-end");
        }
        IEnumerator Performance(int count,bool avoidance)
        {
            var w=Spawn(64,40,count,avoidance);view.Configure(w);yield return null;
            var result=new FrameCase{name="agents-"+count+(avoidance?"-reserved":"-route-only"),agents=count,avoidance=avoidance,minimumActive=count,maximumActive=count};
            report.cases.Add(result);report.width=64;report.height=40;report.phase=result.name;
            double start=Time.realtimeSinceStartupAsDouble,previous=start,accumulator=0,measureStart=0;bool a=false,b=false,c=false;ulong lastStamp=0;
            int gc0=0,gc1=0,gc2=0;var timer=new Stopwatch();
            while(Time.realtimeSinceStartupAsDouble-start<7)
            {
                yield return null;double now=Time.realtimeSinceStartupAsDouble,dt=now-previous;previous=now;
                bool measuring=now-start>=1;
                if(measuring&&measureStart==0){measureStart=now;gc0=GC.CollectionCount(0);gc1=GC.CollectionCount(1);gc2=GC.CollectionCount(2);}
                timer.Restart();double phase=now-start-1;
                if(measuring&&phase>=1.5&&!a){result.events.Add(Change(w,w.doorA,true,"close-main"));a=true;}
                if(measuring&&phase>=3&&!b){result.events.Add(Change(w,10*64+23,true,"place-crate"));b=true;}
                if(measuring&&phase>=4.5&&!c){result.events.Add(Change(w,w.doorA,false,"reopen-main"));c=true;}
                accumulator+=dt;int steps=0;
                while(accumulator>=Tick&&steps<8){w.Step(Tick);accumulator-=Tick;steps++;}
                view.Sync();timer.Stop();
                FrameTimingManager.CaptureFrameTimings();uint available=FrameTimingManager.GetLatestTimings(1,timings);
                if(!measuring)continue;
                int active=count-w.arrived;result.minimumActive=Math.Min(result.minimumActive,active);result.maximumActive=Math.Max(result.maximumActive,active);
                result.maximumBacklog=Math.Max(result.maximumBacklog,accumulator);
                result.frames.Add(new DynamicFrame{frame=Time.frameCount,wallIntervalMs=dt*1000,steps=steps,active=active,pending=w.pendingCount,updateMs=timer.Elapsed.TotalMilliseconds,backlogSeconds=accumulator});
                if(available>0&&timings[0].frameStartTimestamp>lastStamp)
                {
                    var t=timings[0];lastStamp=t.frameStartTimestamp;
                    result.engineFrames.Add(new EngineFrame{timestamp=lastStamp,cpuMs=t.cpuFrameTime,mainMs=t.cpuMainThreadFrameTime,renderMs=t.cpuRenderThreadFrameTime,presentWaitMs=t.cpuMainThreadPresentWaitTime,gpuMs=t.gpuFrameTime});
                }
            }
            result.measuredSeconds=previous-measureStart;result.rebuilds=w.rebuilds;
            result.gen0=GC.CollectionCount(0)-gc0;result.gen1=GC.CollectionCount(1)-gc1;result.gen2=GC.CollectionCount(2)-gc2;
            if(result.minimumActive!=count||result.events.Count!=3||result.frames.Count<100)report.failures++;
            bool gpu=false,render=false;foreach(var timing in result.engineFrames){gpu|=timing.gpuMs>0;render|=timing.renderMs>0;}
            if(result.engineFrames.Count<60||!gpu||!render)
            {report.failures++;Debug.LogError("DYNAMIC_FRAME_COUNTERS_MISSING "+result.name+" requires real rendered player CPU/GPU samples");}
            Capture(result.name);
        }
        void Update()
        {
            if(automated||view==null||view.world==null||paused)return;
            interactiveAccumulator+=Time.unscaledDeltaTime;int steps=0;
            while(interactiveAccumulator>=Tick&&steps<8){view.world.Step(Tick);interactiveAccumulator-=Tick;steps++;}
            view.Sync();
        }
        void Save(string phase){report.phase=phase;File.WriteAllText(reportPath,JsonUtility.ToJson(report,true));}
        void Capture(string suffix)
        {
            string path=Path.ChangeExtension(reportPath,null)+"-"+suffix+".png";
            var camera=Camera.main;var target=new RenderTexture(1280,720,24);var previous=RenderTexture.active;var old=camera.targetTexture;
            camera.targetTexture=target;camera.Render();RenderTexture.active=target;var picture=new Texture2D(1280,720,TextureFormat.RGB24,false);
            picture.ReadPixels(new Rect(0,0,1280,720),0,0);picture.Apply();File.WriteAllBytes(path,picture.EncodeToPNG());
            camera.targetTexture=old;RenderTexture.active=previous;Destroy(picture);target.Release();Destroy(target);
        }
        void OnGUI()
        {
            if(view==null||view.world==null||report==null)return;var w=view.world;
            GUI.Box(new Rect(10,10,510,220),"DYNAMIC FIELD / CELL RESERVATION");
            GUI.Label(new Rect(24,38,490,24),report.phase+" | active "+(w.agents.Length-w.arrived)+" arrived "+w.arrived);
            GUI.Label(new Rect(24,63,490,24),"Pending "+w.pendingCount+" solid "+w.closedCount+" | simulation 60 Hz | radius 0.20");
            GUI.enabled=!automated;
            if(GUI.Button(new Rect(24,94,110,30),"Close main"))SetObstacle(w.doorA,true);
            if(GUI.Button(new Rect(144,94,110,30),"Open main"))SetObstacle(w.doorA,false);
            if(GUI.Button(new Rect(264,94,110,30),"Close both")){SetObstacle(w.doorA,true);SetObstacle(w.doorB,true);}
            if(GUI.Button(new Rect(384,94,110,30),"Open both")){SetObstacle(w.doorA,false);SetObstacle(w.doorB,false);}
            if(GUI.Button(new Rect(24,137,110,30),"Move crate"))
            {crate=w.RelocateCrate(crate);view.Sync();}
            if(GUI.Button(new Rect(144,137,110,30),paused?"Resume":"Pause"))TogglePause();
            if(GUI.Button(new Rect(264,137,110,30),"Restart 64")){view.Configure(Spawn(32,24,64));crate=-1;interactiveAccumulator=0;}
            if(GUI.Button(new Rect(384,137,110,30),"Quit"))Application.Quit();
            GUI.enabled=true;GUI.Label(new Rect(24,183,490,24),"Cyan movers | yellow pending (not solid) | gray obstacle | green exit");
        }
    }
}
