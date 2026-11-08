using System;
using UnityEngine;
namespace TechniqueLab
{
    public static class TrafficGeometry
    {
        public const float Margin=.04f;
        public static bool FitsNarrow(float radius)
        {
            if(radius<=0||float.IsNaN(radius)||float.IsInfinity(radius))throw new ArgumentOutOfRangeException("radius");
            return radius+Margin<=.500001f;
        }
        public static double PairGap(Vector2 a0,Vector2 a1,float ra,Vector2 b0,Vector2 b1,float rb)
        {
            double x=a0.x-b0.x,y=a0.y-b0.y,vx=(a1.x-a0.x)-(b1.x-b0.x),vy=(a1.y-a0.y)-(b1.y-b0.y);
            double vv=vx*vx+vy*vy,t=vv>0?Math.Max(0,Math.Min(1,-(x*vx+y*vy)/vv)):0;
            x+=t*vx;y+=t*vy;return Math.Sqrt(x*x+y*y)-ra-rb;
        }
    }
    public sealed class TrafficGate
    {
        public readonly bool[] leased;
        public readonly int[] directions;
        public int phase,active,granted;
        public int switches,grantsEast,grantsWest,maxAdmissionsWithOpposite,maxTicketWaitTicks;
        public bool paused;
        readonly bool[] pending;readonly long[] ticket;readonly int[] requested;
        long sequence;int admissionsWithOpposite;
        public TrafficGate(int count)
        {leased=new bool[count];directions=new int[count];pending=new bool[count];ticket=new long[count];requested=new int[count];}
        public void Request(int id,int direction,int tick=0)
        {
            if(direction!=1&&direction!=-1)throw new ArgumentOutOfRangeException("direction");
            if(leased[id]||pending[id])return;directions[id]=direction;pending[id]=true;ticket[id]=++sequence;requested[id]=tick;
        }
        int Oldest(int direction)
        {int best=-1;for(int i=0;i<pending.Length;i++)if(pending[i]&&(direction==0||directions[i]==direction)&&(best<0||ticket[i]<ticket[best]))best=i;return best;}
        public void Resolve(int tick=0)
        {
            if(paused)return;
            if(active==0)
            {
                int next=phase;
                if(phase==0){int oldest=Oldest(0);if(oldest<0)return;next=directions[oldest];}
                else if(Oldest(-phase)>=0&&(granted>=4||Oldest(phase)<0))next=-phase;
                else if(Oldest(phase)<0&&Oldest(-phase)<0)return;
                if(next!=phase){if(phase!=0)switches++;phase=next;granted=0;admissionsWithOpposite=0;}
            }
            while(true)
            {
                int oldest=Oldest(phase);bool opposite=Oldest(-phase)>=0;
                if(oldest<0||(opposite&&granted>=4))break;
                leased[oldest]=true;pending[oldest]=false;active++;granted++;
                if(phase==1)grantsEast++;else grantsWest++;
                if(opposite){admissionsWithOpposite++;maxAdmissionsWithOpposite=Math.Max(maxAdmissionsWithOpposite,admissionsWithOpposite);}
                maxTicketWaitTicks=Math.Max(maxTicketWaitTicks,tick-requested[oldest]);
            }
        }
        public void Release(int id)
        {if(!leased[id])return;leased[id]=false;directions[id]=0;active--;}
        public bool HasPending(int direction){return Oldest(direction)>=0;}
    }
}
