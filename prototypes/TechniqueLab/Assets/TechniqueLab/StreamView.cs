using UnityEngine;
namespace TechniqueLab
{
    public sealed class StreamView:MonoBehaviour
    {
        public Material[] materials;public StreamWorld world;public Camera displayCamera;
        Transform root;readonly Transform[] bodies=new Transform[256];readonly Renderer[] renderers=new Renderer[256];readonly int[] identities=new int[256];
        Transform Shape(string label,Vector3 p,Vector3 scale,int color,bool wall=false,PrimitiveType type=PrimitiveType.Cube)
        {var go=GameObject.CreatePrimitive(type);go.name=label;go.transform.SetParent(root);go.transform.position=p;go.transform.localScale=scale;go.GetComponent<Renderer>().sharedMaterial=materials[color];go.layer=wall?12:0;
            if(!wall){go.GetComponent<Collider>().enabled=false;Destroy(go.GetComponent<Collider>());}return go.transform;}
        public void Configure(StreamWorld w)
        {
            if(root!=null){root.gameObject.SetActive(false);Destroy(root.gameObject);}world=w;root=new GameObject("Unlaned stream").transform;root.SetParent(transform);
            displayCamera.orthographic=true;displayCamera.orthographicSize=28;displayCamera.transform.position=new Vector3(23.25f,65,17.25f);displayCamera.transform.rotation=Quaternion.Euler(90,0,0);
            Shape("Ground",new Vector3(23.25f,-.15f,17.25f),new Vector3(48,.1f,36),0);
            for(int node=0;node<StreamMap.N;node++)if(w.map.blocked[node]){var p=w.map.Point(node);Shape("Obstacle "+node,new Vector3(p.x,.5f,p.y),new Vector3(1.5f,1,1.5f),1,true);}
            foreach(int portal in w.map.portals){var p=w.map.Point(portal);Shape("Spawn / exit",new Vector3(p.x,.02f,p.y),new Vector3(.8f,.04f,.8f),4);}
            for(int slot=0;slot<bodies.Length;slot++){bodies[slot]=Shape("Pooled disc",Vector3.zero,Vector3.one,2,false,PrimitiveType.Cylinder);renderers[slot]=bodies[slot].GetComponent<Renderer>();identities[slot]=-1;bodies[slot].gameObject.SetActive(false);}
            Sync(0);
        }
        public void Sync(float fraction)
        {
            for(int slot=0;slot<bodies.Length;slot++)
            {var job=world.slots[slot];bool on=job!=null;if(bodies[slot].gameObject.activeSelf!=on)bodies[slot].gameObject.SetActive(on);if(!on)continue;
                if(identities[slot]!=job.id){identities[slot]=job.id;bodies[slot].name="Request "+job.id+" radius "+job.radius;bodies[slot].localScale=new Vector3(job.radius*2,.4f,job.radius*2);renderers[slot].sharedMaterial=materials[job.start%32<16?2:3];}
                var p=world.Position(job,fraction);bodies[slot].position=new Vector3(p.x,.5f,p.y);}
            Physics.SyncTransforms();
        }
        public int NativeWallHits(float fraction)
        {int n=0;foreach(var job in world.active){var body=bodies[job.slot];float radius=Mathf.Max(body.lossyScale.x,body.lossyScale.z)*.5f;if(Physics.CheckSphere(body.position,radius-.0001f,1<<12,QueryTriggerInteraction.Ignore))n++;}return n;}
        public int MappingErrors(float fraction)
        {int n=0;foreach(var job in world.active){var body=bodies[job.slot];var p=world.Position(job,fraction);if(Vector3.Distance(body.position,new Vector3(p.x,.5f,p.y))>.0001f||Mathf.Abs(body.lossyScale.x*.5f-job.radius)>.0001f||Mathf.Abs(body.lossyScale.z*.5f-job.radius)>.0001f)n++;}return n;}
        public int VisibleCount(){int n=0;foreach(var renderer in renderers)if(renderer.gameObject.activeSelf&&renderer.isVisible)n++;return n;}
    }
}
