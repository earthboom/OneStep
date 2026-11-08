using System;
using UnityEngine;

namespace TechniqueLab
{
    public sealed class CrowdAgent
    {
        public int id,cell=-1,next=-1;
        public Vector2 position;
        public bool arrived;
        public float waited;
    }
    public sealed class CrowdWorld
    {
        public const float Radius=.20f,Speed=3f;
        public readonly int width,height,goal,doorA,doorB;
        public readonly CrowdAgent[] agents;
        public int revision {get{return graph.Revision;}}
        public int rebuilds,closedCount,pendingCount,arrived,alternateCrossings,ticks;
        public bool avoidance=true;
        readonly WeightedGraph graph;
        readonly WeightedField field;
        readonly bool[] permanent,solid,pending,requested;
        readonly int[] owner;
        readonly int[] offsets;
        public CrowdWorld(int width,int height,int count)
        {
            if(width<8||height<8||count<0)throw new ArgumentOutOfRangeException();
            this.width=width;this.height=height;goal=(height/2)*width+width-2;
            doorA=(height/4)*width+width/2;doorB=(height*3/4)*width+width/2;
            int size=width*height;graph=new WeightedGraph(size);field=new WeightedField(size);
            permanent=new bool[size];solid=new bool[size];pending=new bool[size];requested=new bool[size];owner=new int[size];
            offsets=new[]{1,width,-width,-1};
            for(int cell=0;cell<size;cell++)
            {
                owner[cell]=-1;int x=cell%width,y=cell/width;
                permanent[cell]=x==0||y==0||x==width-1||y==height-1||(x==width/2&&cell!=doorA&&cell!=doorB);
                graph.SetBlocked(cell,permanent[cell]);
                if(x+1<width)graph.AddEdge(cell,cell+1,1);
                if(x>0)graph.AddEdge(cell,cell-1,1);
                if(y+1<height)graph.AddEdge(cell,cell+width,1);
                if(y>0)graph.AddEdge(cell,cell-width,1);
                // One exit region: every interior cell on the right strip connects to the same sink.
                // Movers are removed upon reaching the strip; no nonlocal edge is used for motion.
                if(x==width-2&&y>0&&y<height-1&&cell!=goal)graph.AddEdge(cell,goal,0);
            }
            Rebuild();
            agents=new CrowdAgent[count];for(int i=0;i<count;i++)agents[i]=new CrowdAgent{id=i};
        }
        public Vector2 Center(int cell){return new Vector2(cell%width,cell/width);}
        public void Place(int i,int cell)
        {
            if(Solid(cell)||owner[cell]>=0||agents[i].cell>=0)throw new InvalidOperationException("Invalid initial placement");
            agents[i].cell=cell;agents[i].position=Center(cell);owner[cell]=i;
        }
        void Rebuild(){field.Compute(graph,goal);rebuilds++;}
        bool Occupied(int cell)
        {foreach(var a in agents)if(!a.arrived&&(a.cell==cell||a.next==cell))return true;return false;}
        public void Close(int cell)
        {
            if(permanent[cell]||cell==goal)throw new InvalidOperationException("Cannot close permanent wall or goal");
            if(requested[cell])return;
            requested[cell]=true;graph.SetBlocked(cell,true);Rebuild();
            if(Occupied(cell)){pending[cell]=true;pendingCount++;}
            else {solid[cell]=true;closedCount++;}
        }
        public void Open(int cell)
        {
            if(permanent[cell])throw new InvalidOperationException("Cannot open permanent wall");
            if(!requested[cell])return;
            requested[cell]=false;if(pending[cell]){pending[cell]=false;pendingCount--;}
            if(solid[cell]){solid[cell]=false;closedCount--;}
            graph.SetBlocked(cell,false);Rebuild();
        }
        public bool Solid(int cell){return permanent[cell]||solid[cell];}
        public bool Pending(int cell){return pending[cell];}
        public bool RouteBlocked(int cell){return graph.blocked[cell];}
        public bool Fresh {get{return field.IsValidFor(graph);}}
        public int Owner(int cell){return owner[cell];}
        public float Distance(int cell){return field.distance[cell];}
        public int RelocateCrate(int previous)
        {
            if(previous>=0)Open(previous);
            int slots=width/2-3;
            int x=2+(previous<0?0:(previous%width-2+1)%slots);
            int next=(height/4)*width+x;
            Close(next);return next;
        }
        public void Step(float dt)
        {
            if(dt<=0||dt>1f/30||float.IsNaN(dt))throw new ArgumentOutOfRangeException("dt");
            if(!Fresh)throw new InvalidOperationException("Stale route consumed");
            ticks++;
            foreach(var a in agents)
            {
                if(a.arrived||a.cell<0||a.next<0)continue;
                if(Solid(a.next))throw new InvalidOperationException("Committed obstacle on reserved destination");
                a.position=Vector2.MoveTowards(a.position,Center(a.next),Speed*dt);
                if((a.position-Center(a.next)).sqrMagnitude>.00000001f)continue;
                if(avoidance&&owner[a.cell]==a.id)owner[a.cell]=-1;
                a.cell=a.next;a.next=-1;a.waited=0;
                if(a.cell==doorB)alternateCrossings++;
                if(a.cell%width==width-2){a.arrived=true;arrived++;if(avoidance)owner[a.cell]=-1;}
            }
            for(int order=0;order<agents.Length;order++)
            {
                var a=agents[(order+ticks)%agents.Length];if(a.arrived||a.cell<0||a.next>=0)continue;
                int best=-1;float cost=float.PositiveInfinity;
                foreach(int offset in offsets)
                {
                    int n=a.cell+offset;if(n<0||n>=owner.Length||Mathf.Abs(n%width-a.cell%width)+Mathf.Abs(n/width-a.cell/width)!=1)continue;
                    if(graph.blocked[n]||Solid(n)||(avoidance&&owner[n]>=0))continue;
                    float distance=field.distance[n];
                    // Only an already reserved pending-close origin may evacuate from an infinite-distance cell.
                    if(!pending[a.cell]&&!(distance<field.distance[a.cell]))continue;
                    if(distance<cost){cost=distance;best=n;}
                }
                if(best>=0){a.next=best;if(avoidance)owner[best]=a.id;}
                else a.waited+=dt;
            }
            if(pendingCount>0)for(int cell=0;cell<pending.Length;cell++)if(pending[cell]&&!Occupied(cell))
            {pending[cell]=false;pendingCount--;solid[cell]=true;closedCount++;}
        }
    }
}
