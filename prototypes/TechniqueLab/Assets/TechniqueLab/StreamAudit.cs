using System;
using System.Collections.Generic;
using UnityEngine;
namespace TechniqueLab
{
    [Serializable] public sealed class StreamAudit
    {
        public int observations,pairPenetrations,wallPenetrations,teleports,invalidSegments,deadlineViolations;
        public double minimumSurfaceGap=100000,minimumWallGap=100000,maximumGlobalStall,maximumResponseSeconds,maximumPendingSeconds;
        double stall;readonly HashSet<int> late=new HashSet<int>();
        public void Observe(StreamMap map,List<StreamSegment> segments)
        {
            observations++;double movement=0;
            for(int i=0;i<segments.Count;i++)
            {
                var a=segments[i];double dx=(double)a.to.x-a.from.x,dy=(double)a.to.y-a.from.y;movement+=Math.Sqrt(dx*dx+dy*dy);
                if(dx*dx+dy*dy>2.25001)teleports++;
                if(Math.Abs(dx)>.00001&&Math.Abs(dy)>.00001||a.radius<.2f||a.radius>.6f)invalidSegments++;
                for(int cell=0;cell<StreamMap.N;cell++)if(map.blocked[cell])
                {var p=map.Point(cell);double gx=Math.Max(0,Math.Max(p.x-.75-Math.Max(a.from.x,a.to.x),Math.Min(a.from.x,a.to.x)-p.x-.75));
                    double gy=Math.Max(0,Math.Max(p.y-.75-Math.Max(a.from.y,a.to.y),Math.Min(a.from.y,a.to.y)-p.y-.75));
                    double gap=Math.Sqrt(gx*gx+gy*gy)-a.radius;minimumWallGap=Math.Min(minimumWallGap,gap);if(gap<-.0001)wallPenetrations++;}
                for(int j=0;j<i;j++)
                {
                    var b=segments[j];double x=(double)a.from.x-b.from.x,y=(double)a.from.y-b.from.y;
                    double vx=dx-((double)b.to.x-b.from.x),vy=dy-((double)b.to.y-b.from.y),vv=vx*vx+vy*vy;
                    double t=vv>0?Math.Max(0,Math.Min(1,-(x*vx+y*vy)/vv)):0;
                    x+=t*vx;y+=t*vy;double gap=Math.Sqrt(x*x+y*y)-(double)a.radius-b.radius;
                    minimumSurfaceGap=Math.Min(minimumSurfaceGap,gap);if(gap<-.0001)pairPenetrations++;
                }
            }
            stall=segments.Count>0&&movement<.000001?stall+.5:0;maximumGlobalStall=Math.Max(maximumGlobalStall,stall);
        }
        public void Watch(StreamWorld w,int deadline=480)
        {
            foreach(var j in w.jobs)
            {
                if(j.rejected>=0)continue;int age=(j.completed>=0?j.completed:w.epoch)-j.requested;
                maximumResponseSeconds=Math.Max(maximumResponseSeconds,age*.5);
                if(j.admitted<0)maximumPendingSeconds=Math.Max(maximumPendingSeconds,age*.5);
                if(age>deadline&&late.Add(j.id))deadlineViolations++;
            }
        }
        public bool GeometrySafe {get{return pairPenetrations+wallPenetrations+teleports+invalidSegments==0;}}
    }
}
