using System;
using UnityEngine;
namespace TechniqueLab
{
    public static class StreamKernel
    {
        public static double Gap(Vector2 a,Vector2 b,float ar,Vector2 c,Vector2 d,float br)
        {double x=(double)a.x-c.x,y=(double)a.y-c.y,dx=(double)b.x-a.x-d.x+c.x,dy=(double)b.y-a.y-d.y+c.y;
            double v=dx*dx+dy*dy,t=v>0?Math.Max(0,Math.Min(1,-(x*dx+y*dy)/v)):0;
            x+=t*dx;y+=t*dy;return Math.Sqrt(x*x+y*y)-ar-br;}
        public static bool Overdue(int now,int requested,int limit){return now-requested>limit;}
    }
}
