using System;
using UnityEngine;

namespace TechniqueLab
{
    // Independent geometric observations, not an assertion of the reservation table's own answer.
    [Serializable] public sealed class CrowdAudit
    {
        public int observations,pairPenetrations,wallPenetrations,teleports,reservationErrors,staleReads;
        public float minimumSeparation=100000,maximumStep;
        Vector2[] previous;
        bool[] previousActive;
        public CrowdAudit(CrowdWorld world){previous=new Vector2[world.agents.Length];previousActive=new bool[world.agents.Length];Snapshot(world);}
        void Snapshot(CrowdWorld w)
        {for(int i=0;i<previous.Length;i++){previous[i]=w.agents[i].position;previousActive[i]=!w.agents[i].arrived&&w.agents[i].cell>=0;}}
        public void Observe(CrowdWorld w,float dt)
        {
            observations++;if(!w.Fresh)staleReads++;
            for(int i=0;i<previous.Length;i++)
            {
                var a=w.agents[i];float step=Vector2.Distance(previous[i],a.position);maximumStep=Mathf.Max(maximumStep,step);
                if(step>CrowdWorld.Speed*dt+.0002f)teleports++;
                if(a.cell<0||(a.arrived&&!previousActive[i]))continue;
                if(!a.arrived&&w.avoidance&&(w.Owner(a.cell)!=a.id||(a.next>=0&&w.Owner(a.next)!=a.id)))reservationErrors++;
                int x=Mathf.RoundToInt(a.position.x),y=Mathf.RoundToInt(a.position.y);
                for(int z=y-1;z<=y+1;z++)for(int k=x-1;k<=x+1;k++)
                {
                    if(k<0||z<0||k>=w.width||z>=w.height)continue;
                    if(!w.Solid(z*w.width+k))continue;
                    float dx=Mathf.Max(Mathf.Abs(a.position.x-k)-.5f,0),dy=Mathf.Max(Mathf.Abs(a.position.y-z)-.5f,0);
                    if(dx*dx+dy*dy<(CrowdWorld.Radius-.0001f)*(CrowdWorld.Radius-.0001f))wallPenetrations++;
                }
                for(int j=0;j<i;j++)
                {
                    var b=w.agents[j];if(b.cell<0||(b.arrived&&!previousActive[j]))continue;
                    // Minimum distance of the two recorded linear step segments at equal normalized time.
                    Vector2 r=previous[i]-previous[j],v=(a.position-previous[i])-(b.position-previous[j]);
                    float t=v.sqrMagnitude>0?Mathf.Clamp01(-Vector2.Dot(r,v)/v.sqrMagnitude):0;
                    float distance=(r+t*v).magnitude;minimumSeparation=Mathf.Min(minimumSeparation,distance);
                    if(distance<2*CrowdWorld.Radius-.0001f)pairPenetrations++;
                }
            }
            Snapshot(w);
        }
        public bool Safe {get{return pairPenetrations+wallPenetrations+teleports+reservationErrors+staleReads==0;}}
    }
}
