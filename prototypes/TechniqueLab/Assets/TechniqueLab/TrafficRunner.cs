using System;
using System.IO;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using UnityEngine;
using Debug=UnityEngine.Debug;
namespace TechniqueLab
{
    [Serializable] public class TrafficEvent
    {public string action;public int frame,tick,leases;public bool paused;public double milliseconds;public float poseChange;}
    [Serializable] public struct TrafficFrame
    {public int frame,steps,active,visible,leases;public double wallIntervalMs,updateMs,backlogSeconds;}
    [Serializable] public class TrafficBehavior
    {
        public string name;public int agents,arrived,eastArrived,westArrived,ticks,nativeSamples,nativeWallHits,wideOpposingTicks,narrowOpposingTicks,redirected,switches,maxBatch,maxTicketWaitTicks,narrowCrossEast,narrowCrossWest,wideCrossEast,wideCrossWest,small,medium,large,profiles,firstEastRequest,firstWestRequest,firstPhase;
        public float simulatedSeconds,maximumWait;public double maximumStall;public bool passed,pauseVerified;
        public TrafficAudit audit;public List<TrafficEvent> events=new List<TrafficEvent>();
    }
    [Serializable] public class TrafficCase
    {
        public string name;public int agents,minimumActive,minimumVisible,gen0,gen1,gen2,small,medium,large,profiles;public bool mixed;
        public double measuredSeconds,maximumBacklog;
        public List<TrafficFrame> frames=new List<TrafficFrame>(16384);
        public List<EngineFrame> engineFrames=new List<EngineFrame>(16384);
        public List<TrafficEvent> events=new List<TrafficEvent>();
    }
    [Serializable] public class TrafficReport
    {
        public int schemaVersion=1,failures,screenWidth,screenHeight,vSync,antiAliasing;
        public string utc,unity,mode,buildGuid,cpu,gpu,graphicsApi,os,phase;
        public bool editor,batch,finished,frameTimingEnabled;public ulong cpuTimerFrequency;
        public CheckResult[] checks;public List<TrafficBehavior> behavior=new List<TrafficBehavior>();public List<TrafficCase> cases=new List<TrafficCase>();
        public string scope="Authored cardinal lanes, 0.20/0.35/0.60 discs, two static-geometry exits, FIFO direction leases. Not free-flow crowd completeness. Whole rendered wall frames; asynchronous CPU/GPU, missing GPU values retained. Behavior audits separate from real-time 60Hz performance.";
    }
    public sealed class TrafficRunner:MonoBehaviour
    {
        public Material[] materials;public TrafficView view;public TrafficReport report;
        const float Tick=1f/60;string path;bool automated,freeze;double accumulator;
        readonly FrameTiming[] timings=new FrameTiming[1];
        void Error(string message,string stack,LogType type)
        {if(type==LogType.Error||type==LogType.Exception){report.failures++;File.WriteAllText(path+".error.txt",message+"\n"+stack);}}
        IEnumerator Start()
        {
            automated=Application.isBatchMode||Array.IndexOf(Environment.GetCommandLineArgs(),"-trafficRun")>=0;
            Application.runInBackground=true;QualitySettings.vSyncCount=0;Application.targetFrameRate=60;
            path=Path.GetFullPath(Path.Combine(Application.dataPath,Application.isEditor?"../Results/Traffic":"../../Results/Traffic",LabRunner.Argument("-labReport","traffic-ui.json")));
            Directory.CreateDirectory(Path.GetDirectoryName(path));
            report=new TrafficReport{utc=DateTime.UtcNow.ToString("o"),unity=Application.unityVersion,mode=Application.isEditor?"Editor PlayMode":"Windows release Mono",editor=Application.isEditor,batch=Application.isBatchMode,
                buildGuid=Application.buildGUID,cpu=SystemInfo.processorType,gpu=SystemInfo.graphicsDeviceName,graphicsApi=SystemInfo.graphicsDeviceType.ToString(),os=SystemInfo.operatingSystem,
                screenWidth=Screen.width,screenHeight=Screen.height,vSync=QualitySettings.vSyncCount,antiAliasing=QualitySettings.antiAliasing,
                cpuTimerFrequency=FrameTimingManager.GetCpuTimerFrequency(),frameTimingEnabled=FrameTimingManager.IsFeatureEnabled(),phase="initializing"};
            Application.logMessageReceived+=Error;view=gameObject.AddComponent<TrafficView>();view.materials=materials;view.displayCamera=Camera.main;
            if(!automated){view.Configure(TrafficWorld.Dense(64,true));report.phase="interactive";yield break;}
            var checks=TrafficChecks.Run();report.checks=checks.ToArray();report.failures+=checks.FindAll(c=>!c.passed).Count;Save("checks");
            foreach(string name in new[]{"narrow-headon","wide-opposing","large-redirect","mixed-64","mixed-128","mixed-256","reverse-128","late-west-64","admission-pause","deadlock-control","collision-control"})
            {yield return Behavior(name);Save("behavior-"+name);}
            Application.targetFrameRate=-1;int order=LabRunner.Argument("-trafficOrder","0")=="1"?1:0;
            foreach(int count in Application.isEditor?new int[0]:new[]{64,128,256})for(int variant=0;variant<2;variant++)
            {yield return Performance(count,(order+variant)%2==0);Save("frames-"+count+"-"+variant);}
            report.finished=true;Save("finished");Application.logMessageReceived-=Error;Debug.Log("TRAFFIC_FINISHED failures="+report.failures);
            #if UNITY_EDITOR
            UnityEditor.EditorApplication.Exit(report.failures==0?0:2);
            #else
            Application.Quit(report.failures==0?0:2);
            #endif
        }
        TrafficEvent PauseAdmission(bool paused,string action)
        {
            var w=view.world;var before=new Vector2[w.agents.Length];for(int i=0;i<before.Length;i++)before[i]=w.agents[i].position;
            var timer=Stopwatch.StartNew();w.gate.paused=paused;view.Sync();timer.Stop();
            var e=new TrafficEvent{action=action,frame=Time.frameCount,tick=w.ticks,paused=paused,leases=w.gate.active,milliseconds=timer.Elapsed.TotalMilliseconds};
            for(int i=0;i<before.Length;i++)e.poseChange=Mathf.Max(e.poseChange,Vector2.Distance(before[i],w.agents[i].position));
            if(e.poseChange>0)report.failures++;return e;
        }
        IEnumerator Behavior(string name)
        {
            TrafficWorld w;
            if(name=="narrow-headon")w=TrafficWorld.Pair(false);
            else if(name=="wide-opposing")w=TrafficWorld.Pair(true);
            else if(name=="large-redirect")w=TrafficWorld.Pair(false,largeProbe:true);
            else if(name=="deadlock-control")w=TrafficWorld.Pair(false,false,true);
            else if(name=="collision-control")w=TrafficWorld.Pair(false,false,false);
            else w=TrafficWorld.Dense(name=="mixed-256"?256:name=="mixed-128"||name=="reverse-128"?128:64,true,name=="reverse-128");
            if(name=="late-west-64")w.westRequestNotBeforeTick=90;
            view.Configure(w);yield return null;
            var result=new TrafficBehavior{name=name,agents=w.agents.Length,audit=new TrafficAudit(w)};report.behavior.Add(result);report.phase=name;
            bool paused=false,resumed=false,captured=false;int grantsAtPause=0;
            float limit=w.agents.Length==256?300:w.agents.Length==2?120:180;
            if(name.EndsWith("control"))limit=20;
            while(w.ticks*Tick<limit&&w.arrived<w.agents.Length)
            {
                for(int batch=0;batch<8&&w.arrived<w.agents.Length&&w.ticks*Tick<limit;batch++)
                {
                    float time=w.ticks*Tick;
                    if(name=="admission-pause")
                    {
                        if(!paused&&time>=2){result.events.Add(PauseAdmission(true,"pause-admission"));paused=true;grantsAtPause=w.gate.grantsEast+w.gate.grantsWest;}
                        if(paused&&!resumed&&time>=8)
                        {result.pauseVerified=w.gate.active==0&&grantsAtPause==w.gate.grantsEast+w.gate.grantsWest&&(w.gate.HasPending(1)||w.gate.HasPending(-1));
                            result.events.Add(PauseAdmission(false,"resume-admission"));resumed=true;}
                    }
                    w.Step(Tick);result.audit.Observe(w,Tick);
                    if(name=="deadlock-control"&&w.stallSeconds>=5)break;
                    if(name=="collision-control"&&result.audit.pairPenetrations>0)break;
                }
                view.Sync();result.nativeWallHits+=view.NativeWallHits();result.nativeSamples+=w.agents.Length-w.arrived;
                if(!captured&&(name=="wide-opposing"?w.wideOpposingTicks>0:w.ticks*Tick>=10))
                {Capture(name+"-active");captured=true;}
                yield return null;
                if(name=="deadlock-control"&&w.stallSeconds>=5)break;
                if(name=="collision-control"&&result.audit.pairPenetrations>0)break;
            }
            result.arrived=w.arrived;result.eastArrived=w.eastArrived;result.westArrived=w.westArrived;result.ticks=w.ticks;result.simulatedSeconds=w.ticks*Tick;
            result.wideOpposingTicks=w.wideOpposingTicks;result.narrowOpposingTicks=w.narrowOpposingTicks;result.redirected=w.redirected;result.switches=w.gate.switches;
            result.maxBatch=w.gate.maxAdmissionsWithOpposite;result.maxTicketWaitTicks=w.gate.maxTicketWaitTicks;result.maximumWait=w.maximumWait;result.maximumStall=w.maxStallSeconds;
            result.narrowCrossEast=w.narrowCrossEast;result.narrowCrossWest=w.narrowCrossWest;result.wideCrossEast=w.wideCrossEast;result.wideCrossWest=w.wideCrossWest;result.profiles=w.ProfileCount;
            foreach(var a in w.agents){if(a.radius<.3f)result.small++;else if(a.radius<.5f)result.medium++;else result.large++;}
            result.firstEastRequest=w.firstEastRequest;result.firstWestRequest=w.firstWestRequest;result.firstPhase=w.firstPhase;
            bool pass=result.audit.Safe&&result.nativeWallHits==0&&w.arrived==w.agents.Length&&w.eastArrived==w.agents.Length/2&&w.westArrived==w.agents.Length/2&&w.narrowOpposingTicks==0&&w.maxStallSeconds<5&&result.maxBatch<=4;
            if(name=="wide-opposing")pass&=w.wideOpposingTicks>0;
            if(name=="narrow-headon")pass&=w.narrowCrossEast==1&&w.narrowCrossWest==1&&w.gate.switches>0;
            if(name=="large-redirect")pass&=w.redirected==1;
            if(name=="admission-pause")pass&=result.pauseVerified&&resumed;
            if(w.agents.Length>=64)pass&=result.small>0&&result.medium>0&&result.large>0&&result.profiles==3&&w.narrowCrossEast==w.agents.Length/8&&w.narrowCrossWest==w.agents.Length/8;
            if(name=="reverse-128")pass&=w.firstPhase==-1;
            if(name=="late-west-64")pass&=w.firstEastRequest==1&&w.firstWestRequest>=90;
            if(name=="deadlock-control")pass=result.audit.Safe&&w.stallSeconds>=5&&w.arrived<2;
            if(name=="collision-control")pass=result.audit.pairPenetrations>0;
            result.passed=pass;if(!pass)report.failures++;Capture(name+"-end");
        }
        IEnumerator Performance(int count,bool mixed)
        {
            var w=TrafficWorld.Dense(count,mixed);view.Configure(w);yield return null;
            var result=new TrafficCase{name="agents-"+count+(mixed?"-mixed":"-uniform"),agents=count,mixed=mixed,minimumActive=count,minimumVisible=count};report.cases.Add(result);report.phase=result.name;
            result.profiles=w.ProfileCount;foreach(var agent in w.agents){if(agent.radius<.3f)result.small++;else if(agent.radius<.5f)result.medium++;else result.large++;}
            double start=Time.realtimeSinceStartupAsDouble,previous=start,measure=0,backlog=0;bool paused=false,resumed=false;ulong stamp=0;int g0=0,g1=0,g2=0;var timer=new Stopwatch();
            while(Time.realtimeSinceStartupAsDouble-start<7)
            {
                yield return null;double now=Time.realtimeSinceStartupAsDouble,dt=now-previous;previous=now;bool recording=now-start>=1;
                if(recording&&measure==0){measure=now;g0=GC.CollectionCount(0);g1=GC.CollectionCount(1);g2=GC.CollectionCount(2);}
                timer.Restart();double phase=now-start-1;
                if(recording&&phase>=1.5&&!paused){result.events.Add(PauseAdmission(true,"pause-admission"));paused=true;}
                if(recording&&phase>=3&&!resumed){result.events.Add(PauseAdmission(false,"resume-admission"));resumed=true;}
                backlog+=dt;int steps=0;while(backlog>=Tick&&steps<8){w.Step(Tick);backlog-=Tick;steps++;}view.Sync();timer.Stop();
                FrameTimingManager.CaptureFrameTimings();uint n=FrameTimingManager.GetLatestTimings(1,timings);
                if(!recording)continue;int active=count-w.arrived,visible=view.VisibleCount();result.minimumActive=Math.Min(result.minimumActive,active);result.minimumVisible=Math.Min(result.minimumVisible,visible);result.maximumBacklog=Math.Max(result.maximumBacklog,backlog);
                result.frames.Add(new TrafficFrame{frame=Time.frameCount,steps=steps,active=active,visible=visible,leases=w.gate.active,wallIntervalMs=dt*1000,updateMs=timer.Elapsed.TotalMilliseconds,backlogSeconds=backlog});
                if(n>0&&timings[0].frameStartTimestamp>stamp)
                {var t=timings[0];stamp=t.frameStartTimestamp;result.engineFrames.Add(new EngineFrame{timestamp=stamp,cpuMs=t.cpuFrameTime,mainMs=t.cpuMainThreadFrameTime,renderMs=t.cpuRenderThreadFrameTime,presentWaitMs=t.cpuMainThreadPresentWaitTime,gpuMs=t.gpuFrameTime});}
            }
            result.measuredSeconds=previous-measure;result.gen0=GC.CollectionCount(0)-g0;result.gen1=GC.CollectionCount(1)-g1;result.gen2=GC.CollectionCount(2)-g2;
            bool gpu=false,render=false;foreach(var t in result.engineFrames){gpu|=t.gpuMs>0;render|=t.renderMs>0;}
            if(result.minimumActive!=count||result.minimumVisible!=count||result.frames.Count<100||result.engineFrames.Count<60||!gpu||!render||result.events.Count!=2)
            {report.failures++;Debug.LogError("TRAFFIC_FRAME_ACCEPTANCE_FAILED "+result.name);}
            Capture(result.name);
        }
        void Update()
        {
            if(automated||view==null||view.world==null||freeze)return;accumulator+=Time.unscaledDeltaTime;int steps=0;
            while(accumulator>=Tick&&steps<8){view.world.Step(Tick);accumulator-=Tick;steps++;}view.Sync();
        }
        void Save(string phase){report.phase=phase;File.WriteAllText(path,JsonUtility.ToJson(report,true));}
        void Capture(string suffix)
        {
            var camera=Camera.main;var texture=new RenderTexture(1280,720,24);var previous=RenderTexture.active;var old=camera.targetTexture;
            camera.targetTexture=texture;camera.Render();RenderTexture.active=texture;var image=new Texture2D(1280,720,TextureFormat.RGB24,false);image.ReadPixels(new Rect(0,0,1280,720),0,0);image.Apply();
            File.WriteAllBytes(Path.ChangeExtension(path,null)+"-"+suffix+".png",image.EncodeToPNG());camera.targetTexture=old;RenderTexture.active=previous;Destroy(image);texture.Release();Destroy(texture);
        }
        void OnGUI()
        {
            if(view==null||view.world==null||report==null)return;var w=view.world;
            GUI.Box(new Rect(10,10,760,152),"BIDIRECTIONAL / RADIUS-AWARE TRAFFIC");
            GUI.Label(new Rect(24,36,730,24),report.phase+" | active "+(w.agents.Length-w.arrived)+" | east/west arrived "+w.eastArrived+" / "+w.westArrived);
            GUI.Label(new Rect(24,61,730,24),"Narrow phase "+w.gate.phase+" leases "+w.gate.active+" switches "+w.gate.switches+" | radii .20 / .35 / .60 | cyan east / red west");
            GUI.enabled=!automated;
            if(GUI.Button(new Rect(24,94,140,30),w.gate.paused?"Resume admission":"Pause admission"))PauseAdmission(!w.gate.paused,"UI admission");
            if(GUI.Button(new Rect(176,94,140,30),"Restart mixed 64")){view.Configure(TrafficWorld.Dense(64,true));accumulator=0;}
            if(GUI.Button(new Rect(328,94,140,30),freeze?"Resume motion":"Freeze motion"))freeze=!freeze;
            if(GUI.Button(new Rect(480,94,140,30),"Quit"))Application.Quit();GUI.enabled=true;
        }
    }
}
