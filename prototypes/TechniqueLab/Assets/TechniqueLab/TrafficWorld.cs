using System;
using System.Collections.Generic;
using UnityEngine;
namespace TechniqueLab
{
    [Serializable] public struct TrafficWall
    {public float x0,x1,y0,y1;public TrafficWall(float x0,float x1,float y0,float y1){this.x0=x0;this.x1=x1;this.y0=y0;this.y1=y1;}}
    public sealed class TrafficAgent
    {
        public int id,direction,stage,group;
        public float radius,waited;
        public bool narrow,arrived,crossed;
        public Vector2 position;
        public Vector2[] path;
    }
    public sealed class TrafficProfile
    {
        readonly WeightedGraph graph=new WeightedGraph(4);
        readonly WeightedField east=new WeightedField(4),west=new WeightedField(4);
        public TrafficProfile(float radius)
        {
            graph.AddEdge(0,2,1);graph.AddEdge(2,0,1);graph.AddEdge(2,1,1);graph.AddEdge(1,2,1);
            graph.AddEdge(0,3,2);graph.AddEdge(3,0,2);graph.AddEdge(3,1,2);graph.AddEdge(1,3,2);
            graph.SetBlocked(2,!TrafficGeometry.FitsNarrow(radius));
            east.Compute(graph,1);west.Compute(graph,0);
        }
        public bool SelectNarrow(int direction,bool preferNarrow)
        {var field=direction==1?east:west;return preferNarrow&&field.Next(graph,direction==1?0:1)==2;}
    }
    public sealed class TrafficWorld
    {
        public const int Width=128,Height=40;
        public const float Speed=3,LeftMouth=58,RightMouth=70;
        public readonly TrafficAgent[] agents;
        public readonly TrafficGate gate;
        public readonly TrafficWall[] walls;
        public bool gateEnabled=true,pairGuard=true,bruteNeighbors;
        public int ticks,arrived,eastArrived,westArrived,redirected,wideOpposingTicks,narrowOpposingTicks,narrowCrossEast,narrowCrossWest,wideCrossEast,wideCrossWest,westRequestNotBeforeTick,firstEastRequest=-1,firstWestRequest=-1,firstPhase;
        public double travel,stallSeconds,maxStallSeconds;
        public float maximumWait;
        readonly Vector2[] proposal;
        readonly int[] heads=new int[64*20],links;
        readonly Dictionary<float,TrafficProfile> profiles=new Dictionary<float,TrafficProfile>();
        public int ProfileCount {get{return profiles.Count;}}
        TrafficWorld(int count)
        {
            agents=new TrafficAgent[count];proposal=new Vector2[count];links=new int[count];gate=new TrafficGate(count);
            var geometry=new List<TrafficWall>{new TrafficWall(-.5f,127.5f,-.5f,.5f),new TrafficWall(-.5f,127.5f,38.5f,39.5f),
                new TrafficWall(-.5f,.5f,-.5f,39.5f),new TrafficWall(126.5f,127.5f,-.5f,39.5f)};
            for(int y=1;y<39;y++)if(y!=9&&(y<22||y>31))geometry.Add(new TrafficWall(63.5f,64.5f,y-.5f,y+.5f));
            walls=geometry.ToArray();
        }
        TrafficProfile Profile(float radius)
        {TrafficProfile profile;if(!profiles.TryGetValue(radius,out profile)){profile=new TrafficProfile(radius);profiles.Add(radius,profile);}return profile;}
        void Place(int id,int direction,float radius,bool narrow,int wideLane,int queue)
        {
            if(radius<.2f||radius>.6f||float.IsNaN(radius))throw new ArgumentOutOfRangeException("radius");
            bool selected=Profile(radius).SelectNarrow(direction,narrow);if(narrow&&!selected)redirected++;
            float x,y;Vector2[] path;
            if(selected)
            {
                x=direction==1?LeftMouth-queue*1.25f:RightMouth+queue*1.25f;y=direction==1?6:12;
                float mouth=direction==1?LeftMouth:RightMouth,other=direction==1?RightMouth:LeftMouth;
                path=new[]{new Vector2(mouth,y),new Vector2(mouth,9),new Vector2(other,9),new Vector2(direction==1?125.5f:2.5f,9)};
            }
            else
            {
                x=direction==1?61-queue*1.25f:67+queue*1.25f;y=wideLane;
                path=new[]{new Vector2(direction==1?125.5f:2.5f,y)};
            }
            agents[id]=new TrafficAgent{id=id,direction=direction,radius=radius,narrow=selected,position=new Vector2(x,y),path=path};
        }
        public static TrafficWorld Dense(int count,bool mixed,bool reverseTickets=false)
        {
            if(count<8||count>256||count%8!=0)throw new ArgumentOutOfRangeException("count");
            var world=new TrafficWorld(count);int narrow=count/8,wide=(count-2*narrow)/4,id=0;
            for(int group=0;group<6;group++)
            {
                int amount=group<2?narrow:wide+((group-2)<(count-2*narrow)%4?1:0),dir=group%2==0?1:-1;
                int lane=group<4?(dir==1?23:25):(dir==1?27:29);
                for(int q=0;q<amount;q++)
                {
                    float radius=!mixed?.35f:group<2?(q%2==0?.2f:.35f):(q%3==0?.2f:q%3==1?.35f:.6f);
                    world.Place(id,dir,radius,group<2,lane,q);world.agents[id].group=group;id++;
                }
            }
            world.priorityOffset=reverseTickets?count/8:0;world.ValidateInitial();return world;
        }
        public static TrafficWorld Pair(bool wide,bool gate=true,bool guard=true,bool largeProbe=false)
        {
            var world=new TrafficWorld(2){gateEnabled=gate,pairGuard=guard};
            world.Place(0,1,largeProbe?.6f:wide?.6f:.35f,!wide,23,0);
            world.Place(1,-1,wide?.2f:.35f,!wide,25,0);
            world.ValidateInitial();return world;
        }
        int priorityOffset;
        void ValidateInitial()
        {
            for(int i=0;i<agents.Length;i++)
            {var a=agents[i];if(WallBlocked(a.position,a.position,a.radius))throw new InvalidOperationException("Initial body intersects wall");
                for(int j=0;j<i;j++)if(TrafficGeometry.PairGap(a.position,a.position,a.radius,agents[j].position,agents[j].position,agents[j].radius)<TrafficGeometry.Margin-.00001)
                    throw new InvalidOperationException("Initial bodies overlap");}
        }
        static bool Slab(float p,float v,float low,float high,ref float enter,ref float leave)
        {
            if(Mathf.Abs(v)<.0000001f)return p>low&&p<high;
            float a=(low-p)/v,b=(high-p)/v;if(a>b){float temp=a;a=b;b=temp;}
            enter=Mathf.Max(enter,a);leave=Mathf.Min(leave,b);return enter<leave;
        }
        bool WallBlocked(Vector2 from,Vector2 to,float radius)
        {
            float r=radius+TrafficGeometry.Margin;var delta=to-from;
            foreach(var wall in walls)
            {float enter=0,leave=1;if(Slab(from.x,delta.x,wall.x0-r,wall.x1+r,ref enter,ref leave)&&
                Slab(from.y,delta.y,wall.y0-r,wall.y1+r,ref enter,ref leave))return true;}
            return false;
        }
        void BuildNeighbors()
        {
            for(int i=0;i<heads.Length;i++)heads[i]=-1;
            for(int i=0;i<agents.Length;i++)if(!agents[i].arrived)
            {var p=agents[i].position;int cell=Mathf.Clamp((int)(p.y/2),0,19)*64+Mathf.Clamp((int)(p.x/2),0,63);links[i]=heads[cell];heads[cell]=i;}
        }
        bool SafePair(int index,Vector2 candidate,int other)
        {
            if(index==other||agents[other].arrived)return true;var a=agents[index];var b=agents[other];
            return TrafficGeometry.PairGap(a.position,candidate,a.radius,b.position,proposal[other],b.radius)>=TrafficGeometry.Margin-.000001;
        }
        bool NeighborSafe(int index,Vector2 candidate)
        {
            if(bruteNeighbors){for(int j=0;j<agents.Length;j++)if(!SafePair(index,candidate,j))return false;return true;}
            var p=agents[index].position;int x=(int)(p.x/2),y=(int)(p.y/2);
            // Max relative reach: 2*.60 + 2*3*(1/30) + .04 = 1.44 < a 2-unit bin.
            for(int z=Math.Max(0,y-1);z<=Math.Min(19,y+1);z++)for(int k=Math.Max(0,x-1);k<=Math.Min(63,x+1);k++)
                for(int j=heads[z*64+k];j>=0;j=links[j])if(!SafePair(index,candidate,j))return false;
            return true;
        }
        public void Step(float dt)
        {
            if(dt<=0||dt>1f/30||float.IsNaN(dt))throw new ArgumentOutOfRangeException("dt");ticks++;
            for(int scan=0;scan<agents.Length;scan++)
            {
                var a=agents[(scan+priorityOffset)%agents.Length];
                if(a.arrived||!a.narrow)continue;
                if(gate.leased[a.id]&&(a.direction==1?a.position.x>RightMouth+a.radius+TrafficGeometry.Margin:a.position.x<LeftMouth-a.radius-TrafficGeometry.Margin))gate.Release(a.id);
                if(gateEnabled&&!gate.leased[a.id]&&a.stage==0&&(a.position-a.path[0]).sqrMagnitude<.000001f&&
                    (a.direction==1||ticks>=westRequestNotBeforeTick))
                {gate.Request(a.id,a.direction,ticks);if(a.direction==1&&firstEastRequest<0)firstEastRequest=ticks;if(a.direction==-1&&firstWestRequest<0)firstWestRequest=ticks;}
            }
            if(gateEnabled){gate.Resolve(ticks);if(firstPhase==0&&gate.phase!=0)firstPhase=gate.phase;}
            for(int i=0;i<agents.Length;i++)proposal[i]=agents[i].position;
            BuildNeighbors();
            for(int order=0;order<agents.Length;order++)
            {
                int index=(order+priorityOffset+ticks)%agents.Length;var a=agents[index];if(a.arrived)continue;
                if((a.position-a.path[a.stage]).sqrMagnitude<.0000001f)
                {
                    if(a.narrow&&a.stage==0&&gateEnabled&&!gate.leased[index])continue;
                    if(a.stage<a.path.Length-1)a.stage++;
                }
                Vector2 candidate=Vector2.MoveTowards(a.position,a.path[a.stage],Speed*dt);
                bool safe=!WallBlocked(a.position,candidate,a.radius);
                if(safe&&pairGuard)safe=NeighborSafe(index,candidate);
                if(safe)proposal[index]=candidate;
            }
            double moved=0;
            foreach(var a in agents)
            {
                if(a.arrived)continue;float distance=Vector2.Distance(a.position,proposal[a.id]);a.position=proposal[a.id];moved+=distance;
                a.waited=distance>0?0:a.waited+dt;maximumWait=Mathf.Max(maximumWait,a.waited);
                if(!a.crossed&&(a.direction==1?a.position.x>=64:a.position.x<=64))
                {a.crossed=true;if(a.narrow){if(a.direction==1)narrowCrossEast++;else narrowCrossWest++;}else{if(a.direction==1)wideCrossEast++;else wideCrossWest++;}}
                if(a.stage==a.path.Length-1&&(a.position-a.path[a.stage]).sqrMagnitude<.0000001f)
                {a.arrived=true;arrived++;if(a.direction==1)eastArrived++;else westArrived++;gate.Release(a.id);}
            }
            travel+=moved;stallSeconds=moved<.000001&&arrived<agents.Length&&!gate.paused?stallSeconds+dt:0;maxStallSeconds=Math.Max(maxStallSeconds,stallSeconds);
            bool we=false,ww=false,ne=false,nw=false;
            foreach(var a in agents)if(!a.arrived)
            {
                if(!a.narrow&&a.position.x+a.radius>=62&&a.position.x-a.radius<=66){if(a.direction==1)we=true;else ww=true;}
                if(a.narrow&&a.position.x+a.radius>LeftMouth&&a.position.x-a.radius<RightMouth&&a.position.y+a.radius>8.5f&&a.position.y-a.radius<9.5f){if(a.direction==1)ne=true;else nw=true;}
            }
            if(we&&ww)wideOpposingTicks++;if(ne&&nw)narrowOpposingTicks++;
        }
    }
}
