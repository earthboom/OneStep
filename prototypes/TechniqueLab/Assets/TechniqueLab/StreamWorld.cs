using System;
using System.Collections.Generic;
using UnityEngine;
namespace TechniqueLab
{
    public sealed class StreamMap
    {
        public const int W=32,H=24,N=W*H;public const float Spacing=1.5f;
        public readonly bool[] blocked=new bool[N];
        readonly Dictionary<int,int[]> distances=new Dictionary<int,int[]>();
        public readonly int layout;public readonly int[] portals={1+6*W,1+17*W,8+22*W,23+22*W,30+17*W,30+6*W,23+W,8+W};
        public StreamMap(int layout)
        {
            this.layout=layout;
            for(int y=0;y<H;y++)for(int x=0;x<W;x++)
            {
                bool wall=x==0||y==0||x==W-1||y==H-1;
                if(layout==0)wall|=x>=10&&x<=11&&y>=4&&y<=15||x>=20&&x<=21&&y>=9&&y<=20;
                if(layout==1)wall|=x==15&&y>0&&y<H-1&&y!=11;
                if(layout==2)wall|=x>=7&&x<=11&&y>=7&&y<=10||x>=20&&x<=24&&y>=14&&y<=17||x>=14&&x<=17&&y>=5&&y<=7;
                blocked[x+y*W]=wall;
            }
        }
        public Vector2 Point(int node){return new Vector2(node%W*Spacing,node/W*Spacing);}
        public int Neighbor(int node,int action)
        {int x=node%W+(action==0?-1:action==1?1:0),y=node/W+(action==2?-1:action==3?1:0);return x<0||x>=W||y<0||y>=H?-1:x+y*W;}
        public int[] Distances(int goal)
        {
            int[] d;if(distances.TryGetValue(goal,out d))return d;d=new int[N];for(int i=0;i<N;i++)d[i]=-1;
            if(goal>=0&&goal<N&&!blocked[goal]){var queue=new int[N];int read=0,write=1;queue[0]=goal;d[goal]=0;
                while(read<write){int u=queue[read++];for(int k=0;k<4;k++){int v=Neighbor(u,k);if(v>=0&&!blocked[v]&&d[v]<0){d[v]=d[u]+1;queue[write++]=v;}}}}
            distances.Add(goal,d);return d;
        }
    }
    public struct StreamReservation {public int from,to,time;public float radius;}
    public sealed class StreamReservations
    {
        readonly StreamMap map;readonly List<int>[] bins=new List<int>[StreamPlanner.Horizon*StreamMap.N];
        readonly List<int> touched=new List<int>();readonly List<StreamReservation> edges=new List<StreamReservation>();
        public bool ignore;
        public StreamReservations(StreamMap map){this.map=map;}
        public void Clear(){foreach(int key in touched)bins[key].Clear();touched.Clear();edges.Clear();}
        void Index(int key,int edge){if(bins[key]==null)bins[key]=new List<int>(4);if(bins[key].Count==0)touched.Add(key);bins[key].Add(edge);}
        public void Add(int[] path,int offset,float radius)
        {for(int t=0;offset+t+1<path.Length;t++){int a=path[offset+t],b=path[offset+t+1],index=edges.Count;
            edges.Add(new StreamReservation{from=a,to=b,time=t,radius=radius});Index(t*StreamMap.N+a,index);if(a!=b)Index(t*StreamMap.N+b,index);}}
        bool Conflict(int time,int a,int b,float radius,int index)
        {var e=edges[index];return e.time==time&&StreamKernel.Gap(map.Point(a),map.Point(b),radius,map.Point(e.from),map.Point(e.to),e.radius)<.04-.000001;}
        public bool Safe(int time,int from,int to,float radius,bool exhaustive=false)
        {
            if(ignore)return true;if(exhaustive){for(int i=0;i<edges.Count;i++)if(Conflict(time,from,to,radius,i))return false;return true;}
            // Cardinal edges are 1.5 units long; max radius sum + margin is 1.24.
            // Every potentially intersecting grid edge has an endpoint in this expanded node box.
            int x0=Math.Max(0,Math.Min(from%32,to%32)-1),x1=Math.Min(31,Math.Max(from%32,to%32)+1);
            int y0=Math.Max(0,Math.Min(from/32,to/32)-1),y1=Math.Min(23,Math.Max(from/32,to/32)+1);
            for(int y=y0;y<=y1;y++)for(int x=x0;x<=x1;x++){var list=bins[time*StreamMap.N+x+y*32];if(list!=null)foreach(int i in list)if(Conflict(time,from,to,radius,i))return false;}
            return true;
        }
    }
    public sealed class StreamPlanner
    {
        public const int Horizon=96;
        readonly StreamMap map;public readonly StreamReservations reservations;
        readonly int[] seen=new int[(Horizon+1)*StreamMap.N],parent=new int[(Horizon+1)*StreamMap.N],heap=new int[(Horizon+1)*StreamMap.N];
        int stamp,size;int[] heuristic;public int expanded;
        public StreamPlanner(StreamMap map){this.map=map;reservations=new StreamReservations(map);}
        bool Less(int a,int b){int da=heuristic[a%StreamMap.N],db=heuristic[b%StreamMap.N];int fa=a/StreamMap.N+da,fb=b/StreamMap.N+db;return fa<fb||fa==fb&&(da<db||da==db&&a<b);}
        void Push(int state){int i=size++;while(i>0){int p=(i-1)/2;if(!Less(state,heap[p]))break;heap[i]=heap[p];i=p;}heap[i]=state;}
        int Pop(){int result=heap[0],last=heap[--size],i=0;while(i*2+1<size){int c=i*2+1;if(c+1<size&&Less(heap[c+1],heap[c]))c++;if(!Less(heap[c],last))break;heap[i]=heap[c];i=c;}heap[i]=last;return result;}
        public int[] Plan(int from,int goal,float radius)
        {
            if(radius<.2f||radius>.6f||float.IsNaN(radius))throw new ArgumentOutOfRangeException("radius");
            expanded=0;if(from<0||from>=StreamMap.N||goal<0||goal>=StreamMap.N||map.blocked[from]||map.blocked[goal])return null;
            heuristic=map.Distances(goal);if(heuristic[from]<0||heuristic[from]+1>Horizon||!reservations.Safe(0,from,from,radius))return null;
            stamp++;size=0;int start=StreamMap.N+from;seen[start]=stamp;parent[start]=-1;Push(start);
            while(size>0)
            {
                int state=Pop(),time=state/StreamMap.N,u=state%StreamMap.N;expanded++;
                if(u==goal){var path=new int[time+1];path[0]=from;for(int s=state;s>=0;s=parent[s])path[s/StreamMap.N]=s%StreamMap.N;return path;}
                if(time==Horizon)continue;
                for(int k=0;k<5;k++)
                {int v=k==4?u:map.Neighbor(u,k);if(v<0||map.blocked[v]||heuristic[v]<0||time+1+heuristic[v]>Horizon)continue;
                    int next=(time+1)*StreamMap.N+v;if(seen[next]==stamp||!reservations.Safe(time,u,v,radius))continue;
                    seen[next]=stamp;parent[next]=state;Push(next);}
            }
            return null;
        }
    }
    [Serializable] public sealed class StreamJob
    {public int id,start,goal,requested,admitted=-1,completed=-1,rejected=-1,slot=-1,routeActions,turns,waitActions,maxWaitActions;public float radius;public string rejection;
        [NonSerialized]public int[] path;[NonSerialized]public int cursor,wait;}
    public struct StreamSegment {public int id;public Vector2 from,to;public float radius;public bool terminal;}
    public sealed class StreamWorld
    {
        public readonly StreamMap map;public readonly StreamPlanner planner;
        public readonly List<StreamJob> jobs=new List<StreamJob>(),active=new List<StreamJob>(),pending=new List<StreamJob>();
        public readonly List<StreamSegment> last=new List<StreamSegment>();
        public int epoch,completed,rejected,maxPending,maxActive,failedPlans,admittedThisEpoch,attemptedThisEpoch;
        public double planningMs;public bool lifo,ignoreReservations,biased,sourcePaused;
        public readonly StreamJob[] slots=new StreamJob[256];
        readonly int rate,inflow,seed;bool begun;
        public StreamWorld(int layout,int rate,int inflow,int seed=0,bool lifo=false,bool unsafeMode=false,bool biased=false)
        {map=new StreamMap(layout);planner=new StreamPlanner(map);this.lifo=lifo;ignoreReservations=unsafeMode;this.biased=biased;this.rate=rate;this.inflow=inflow;this.seed=seed;}
        public StreamJob Request(int start,int goal,float radius){var j=new StreamJob{id=jobs.Count,start=start,goal=goal,radius=radius,requested=epoch};jobs.Add(j);pending.Add(j);return j;}
        public void Begin()
        {
            if(begun)throw new InvalidOperationException("Finish the current action before beginning another");begun=true;
            var timer=System.Diagnostics.Stopwatch.StartNew();admittedThisEpoch=attemptedThisEpoch=0;
            if(epoch<inflow&&!sourcePaused)for(int k=0;k<rate;k++)
            {int id=jobs.Count,p=(id+seed)%8;if(biased&&id%8!=0)p=id%2;
                int q=(p+4+(id/8%3)-1)%8;Request(map.portals[p],map.portals[q],id%3==0?.2f:id%3==1?.35f:.6f);}
            maxPending=Math.Max(maxPending,pending.Count);planner.reservations.Clear();planner.reservations.ignore=ignoreReservations;
            foreach(var j in active)planner.reservations.Add(j.path,j.cursor,j.radius);
            while(pending.Count>0&&active.Count<slots.Length)
            {
                int index=lifo?pending.Count-1:0;var job=pending[index];
                if(map.blocked[job.start]||map.Distances(job.goal)[job.start]<0||map.Distances(job.goal)[job.start]+1>StreamPlanner.Horizon)
                {job.rejected=epoch;job.rejection="unreachable-or-static-route-exceeds-horizon";rejected++;pending.RemoveAt(index);continue;}
                attemptedThisEpoch++;var path=planner.Plan(job.start,job.goal,job.radius);
                if(path==null){failedPlans++;break;}
                pending.RemoveAt(index);job.path=path;job.admitted=epoch;job.routeActions=path.Length-1;
                int previousDirection=0;for(int i=1;i<path.Length;i++)
                {int dir=path[i]-path[i-1];if(dir==0)job.waitActions++;else{if(previousDirection!=0&&dir!=previousDirection)job.turns++;previousDirection=dir;}}
                for(int slot=0;slot<slots.Length;slot++)if(slots[slot]==null){slots[slot]=job;job.slot=slot;break;}
                active.Add(job);planner.reservations.Add(path,0,job.radius);admittedThisEpoch++;
                if(lifo)break;
            }
            maxActive=Math.Max(maxActive,active.Count);timer.Stop();planningMs=timer.Elapsed.TotalMilliseconds;
        }
        public void Finish()
        {
            if(!begun)throw new InvalidOperationException("Begin before advancing");last.Clear();
            for(int i=active.Count-1;i>=0;i--)
            {
                var j=active[i];int a=j.path[j.cursor],b=j.path[++j.cursor];j.wait=a==b?j.wait+1:0;j.maxWaitActions=Math.Max(j.maxWaitActions,j.wait);
                bool done=j.cursor==j.path.Length-1;
                last.Add(new StreamSegment{id=j.id,from=map.Point(a),to=map.Point(b),radius=j.radius,terminal=done});
                if(done){j.completed=epoch+1;completed++;slots[j.slot]=null;active.RemoveAt(i);}
            }
            epoch++;begun=false;
        }
        public Vector2 Position(StreamJob job,float fraction)
        {return Vector2.Lerp(map.Point(job.path[job.cursor]),map.Point(job.path[job.cursor+1]),Mathf.Clamp01(fraction));}
    }
}
