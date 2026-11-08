using System;
using System.Collections.Generic;

namespace TechniqueLab
{
    public struct Edge { public int node; public float cost; public Edge(int node, float cost) { this.node=node; this.cost=cost; } }
    public sealed class WeightedGraph
    {
        public readonly List<Edge>[] outgoing, incoming;
        public readonly bool[] blocked;
        public int Revision { get; private set; }
        public int Count { get { return outgoing.Length; } }
        public int width;
        public float minimumCost = float.PositiveInfinity;
        public WeightedGraph(int count)
        {
            outgoing=new List<Edge>[count]; incoming=new List<Edge>[count]; blocked=new bool[count];
            for(int i=0;i<count;i++) { outgoing[i]=new List<Edge>(); incoming[i]=new List<Edge>(); }
        }
        public void AddEdge(int from,int to,float cost)
        {
            if(cost<0 || float.IsNaN(cost) || float.IsInfinity(cost)) throw new ArgumentOutOfRangeException("cost");
            outgoing[from].Add(new Edge(to,cost)); incoming[to].Add(new Edge(from,cost));
            minimumCost=Math.Min(minimumCost,cost); Revision++;
        }
        public void SetBlocked(int node,bool value) { if(blocked[node]!=value) { blocked[node]=value; Revision++; } }
        public static WeightedGraph Grid(int width)
        {
            var g=new WeightedGraph(width*width); g.width=width;
            for(int z=0;z<width;z++) for(int x=0;x<width;x++)
            {
                int u=z*width+x;
                int[] offsets={-1,1,-width,width};
                for(int k=0;k<4;k++)
                {
                    int nx=x+(k==0?-1:k==1?1:0),nz=z+(k==2?-1:k==3?1:0);
                    if(nx<0||nx>=width||nz<0||nz>=width)continue;
                    int v=u+offsets[k]; g.AddEdge(u,v,1+((nx*13+nz*7)%7==0?4:0));
                }
            }
            for(int z=0;z<width;z++) if(z!=width/2) g.SetBlocked(z*width+width/2,true);
            return g;
        }
    }
    public sealed class WeightedField
    {
        public readonly float[] distance;
        readonly int[] next;
        int revision=-1;
        WeightedGraph owner;
        readonly MinHeap heap=new MinHeap();
        public WeightedField(int count) { distance=new float[count]; next=new int[count]; }
        public void Compute(WeightedGraph graph,int goal)
        {
            for(int i=0;i<distance.Length;i++){ distance[i]=float.PositiveInfinity;next[i]=-1; }
            heap.Clear();revision=graph.Revision;owner=graph;
            if(graph.blocked[goal])return;
            distance[goal]=0;heap.Push(goal,0);
            while(heap.Count>0)
            {
                float priority;int current=heap.Pop(out priority);
                if(priority!=distance[current])continue;
                foreach(var edge in graph.incoming[current])
                {
                    int previous=edge.node;if(graph.blocked[previous])continue;
                    float candidate=priority+edge.cost;
                    // Only strict improvements point to the settled current node; zero-cost ties never overwrite it.
                    if(candidate<distance[previous])
                    {distance[previous]=candidate;next[previous]=current;heap.Push(previous,candidate);}
                }
            }
        }
        public bool IsValidFor(WeightedGraph graph) { return ReferenceEquals(owner,graph)&&revision==graph.Revision; }
        public int Next(WeightedGraph graph,int node)
        { if(!IsValidFor(graph))throw new InvalidOperationException("Stale navigation field");return next[node]; }
    }
    public sealed class AStarWorkspace
    {
        readonly float[] distance;
        readonly MinHeap heap=new MinHeap();
        public AStarWorkspace(int count) { distance=new float[count]; }
        static float Heuristic(WeightedGraph graph,int node,int goal)
        {return graph.width>0?(Math.Abs(node%graph.width-goal%graph.width)+Math.Abs(node/graph.width-goal/graph.width))*graph.minimumCost:0;}
        public float Cost(WeightedGraph graph,int start,int goal)
        {
            if(graph.blocked[start]||graph.blocked[goal])return float.PositiveInfinity;
            for(int i=0;i<distance.Length;i++)distance[i]=float.PositiveInfinity;
            heap.Clear();distance[start]=0;heap.Push(start,Heuristic(graph,start,goal));
            while(heap.Count>0)
            {
                float priority;int current=heap.Pop(out priority);
                if(priority>distance[current]+Heuristic(graph,current,goal))continue;
                if(current==goal)return distance[current];
                foreach(var edge in graph.outgoing[current])
                {
                    if(graph.blocked[edge.node])continue;
                    float candidate=distance[current]+edge.cost;
                    if(candidate<distance[edge.node])
                    {distance[edge.node]=candidate;heap.Push(edge.node,candidate+Heuristic(graph,edge.node,goal));}
                }
            }
            return float.PositiveInfinity;
        }
    }
    internal sealed class MinHeap
    {
        struct Item {public int node;public float priority;}
        Item[] items=new Item[128];
        public int Count{get;private set;}
        public void Clear(){Count=0;}
        public void Push(int node,float priority)
        {
            if(Count==items.Length)Array.Resize(ref items,items.Length*2);
            var item=new Item{node=node,priority=priority};int i=Count++;
            while(i>0){int parent=(i-1)/2;if(items[parent].priority<=priority)break;items[i]=items[parent];i=parent;}
            items[i]=item;
        }
        public int Pop(out float priority)
        {
            var first=items[0];var last=items[--Count];int i=0;
            while(i*2+1<Count)
            {int child=i*2+1;if(child+1<Count&&items[child+1].priority<items[child].priority)child++;
                if(items[child].priority>=last.priority)break;items[i]=items[child];i=child;}
            items[i]=last;priority=first.priority;return first.node;
        }
    }
}
