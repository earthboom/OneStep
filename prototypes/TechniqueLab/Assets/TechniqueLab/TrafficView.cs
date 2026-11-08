using UnityEngine;
namespace TechniqueLab
{
    public sealed class TrafficView:MonoBehaviour
    {
        public Material[] materials;public Camera displayCamera;public TrafficWorld world;
        Transform root;Transform[] movers;Renderer[] renderers;Renderer eastLight,westLight;
        Transform Shape(string name,Vector3 p,Vector3 scale,int color,bool wall=false,PrimitiveType type=PrimitiveType.Cube)
        {
            var go=GameObject.CreatePrimitive(type);go.name=name;go.transform.SetParent(root);go.transform.position=p;go.transform.localScale=scale;
            go.GetComponent<Renderer>().sharedMaterial=materials[color];go.layer=wall?11:0;
            if(!wall){go.GetComponent<Collider>().enabled=false;Destroy(go.GetComponent<Collider>());}return go.transform;
        }
        public void Configure(TrafficWorld w)
        {
            if(root!=null){root.gameObject.SetActive(false);Destroy(root.gameObject);}
            world=w;root=new GameObject("Traffic world").transform;root.SetParent(transform);
            displayCamera.orthographic=true;displayCamera.orthographicSize=TrafficWorld.Width/(2*displayCamera.aspect)*1.08f;
            displayCamera.transform.position=new Vector3(63.5f,65,19.5f);displayCamera.transform.rotation=Quaternion.Euler(90,0,0);
            Shape("Floor",new Vector3(63.5f,-.15f,19.5f),new Vector3(128,.1f,40),0);
            foreach(var b in world.walls)Shape("Wall",new Vector3((b.x0+b.x1)/2,.5f,(b.y0+b.y1)/2),new Vector3(b.x1-b.x0,1,b.y1-b.y0),1,true);
            for(int lane=0;lane<5;lane++)
            {float y=lane==0?9:21+lane*2;Shape("Exit east",new Vector3(125.5f,.05f,y),new Vector3(.5f,.1f,1),4);Shape("Exit west",new Vector3(2.5f,.05f,y),new Vector3(.5f,.1f,1),4);}
            eastLight=Shape("East admission",new Vector3(58,.1f,4),new Vector3(1,.2f,1),5).GetComponent<Renderer>();
            westLight=Shape("West admission",new Vector3(70,.1f,14),new Vector3(1,.2f,1),5).GetComponent<Renderer>();
            movers=new Transform[w.agents.Length];renderers=new Renderer[movers.Length];
            for(int i=0;i<movers.Length;i++)
            {var a=w.agents[i];movers[i]=Shape("Disc "+i+" r="+a.radius,Vector3.zero,new Vector3(2*a.radius,.4f,2*a.radius),a.direction==1?2:3,false,PrimitiveType.Cylinder);renderers[i]=movers[i].GetComponent<Renderer>();}
            Sync();
        }
        public void Sync()
        {
            for(int i=0;i<movers.Length;i++)
            {var a=world.agents[i];movers[i].gameObject.SetActive(!a.arrived);movers[i].position=new Vector3(a.position.x,.5f,a.position.y);}
            eastLight.sharedMaterial=materials[!world.gate.paused&&world.gate.phase==1?4:5];westLight.sharedMaterial=materials[!world.gate.paused&&world.gate.phase==-1?4:5];
            Physics.SyncTransforms();
        }
        public int NativeWallHits()
        {int hits=0;foreach(var a in world.agents)if(!a.arrived&&Physics.CheckSphere(new Vector3(a.position.x,.5f,a.position.y),a.radius-.0001f,1<<11,QueryTriggerInteraction.Ignore))hits++;return hits;}
        public int VisibleCount()
        {int n=0;foreach(var renderer in renderers)if(renderer.gameObject.activeSelf&&renderer.isVisible)n++;return n;}
    }
}
