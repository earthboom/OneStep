using System;
using UnityEngine;
namespace TechniqueLab
{
    [Serializable] public sealed class TrafficAudit
    {
        public int observations,pairPenetrations,wallPenetrations,teleports,wrongLeases,forbiddenNarrow,diagonalSteps;
        public double minimumSurfaceGap=100000,minimumWallGap=100000;
        public float maximumStep;
        readonly Vector2[] previous;readonly bool[] active;
        public TrafficAudit(TrafficWorld w){previous=new Vector2[w.agents.Length];active=new bool[previous.Length];Snapshot(w);}
        void Snapshot(TrafficWorld w){for(int i=0;i<previous.Length;i++){previous[i]=w.agents[i].position;active[i]=!w.agents[i].arrived;}}
        public void Observe(TrafficWorld w,float dt)
        {
            observations++;int leaseDirection=0;
            for(int i=0;i<previous.Length;i++)
            {
                var a=w.agents[i];if(!active[i]&&a.arrived)continue;
                double sx=previous[i].x,sy=previous[i].y,ex=a.position.x,ey=a.position.y;
                double vx=ex-sx,vy=ey-sy,step=Math.Sqrt(vx*vx+vy*vy);maximumStep=Math.Max(maximumStep,(float)step);
                if(step>TrafficWorld.Speed*dt+.0002)teleports++;
                if(Math.Abs(vx)>.00001&&Math.Abs(vy)>.00001)diagonalSteps++;
                if(a.narrow&&a.radius+TrafficGeometry.Margin>.500001f)forbiddenNarrow++;
                if(w.gate.leased[i]){if(leaseDirection!=0&&leaseDirection!=a.direction)wrongLeases++;leaseDirection=a.direction;}
                foreach(var box in w.walls)
                {
                    // Exact minimum of a cardinal segment and an axis-aligned rectangle.
                    double dx=Math.Max(0,Math.Max(box.x0-Math.Max(sx,ex),Math.Min(sx,ex)-box.x1));
                    double dy=Math.Max(0,Math.Max(box.y0-Math.Max(sy,ey),Math.Min(sy,ey)-box.y1));
                    double gap=Math.Sqrt(dx*dx+dy*dy)-a.radius;minimumWallGap=Math.Min(minimumWallGap,gap);if(gap<-.0001)wallPenetrations++;
                }
                for(int j=0;j<i;j++)
                {
                    var b=w.agents[j];if(!active[j]&&b.arrived)continue;
                    double x=sx-previous[j].x,y=sy-previous[j].y,dx=vx-(b.position.x-previous[j].x),dy=vy-(b.position.y-previous[j].y);
                    double sum=a.radius+b.radius,reach=sum+Math.Max(minimumSurfaceGap,0);
                    double x1=x+dx,y1=y+dy;
                    double bx=x*x1<=0?0:Math.Min(Math.Abs(x),Math.Abs(x1)),by=y*y1<=0?0:Math.Min(Math.Abs(y),Math.Abs(y1));
                    if(bx>reach||by>reach)continue;
                    double vv=dx*dx+dy*dy,t=vv>0?Math.Max(0,Math.Min(1,-(x*dx+y*dy)/vv)):0;
                    x+=t*dx;y+=t*dy;double squared=x*x+y*y;
                    if(squared<reach*reach){double gap=Math.Sqrt(squared)-sum;minimumSurfaceGap=Math.Min(minimumSurfaceGap,gap);if(gap<-.0001)pairPenetrations++;}
                }
            }
            Snapshot(w);
        }
        public bool Safe {get{return pairPenetrations+wallPenetrations+teleports+wrongLeases+forbiddenNarrow+diagonalSteps==0;}}
    }
}
