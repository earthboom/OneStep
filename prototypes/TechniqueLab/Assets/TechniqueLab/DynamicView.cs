using UnityEngine;

namespace TechniqueLab
{
    public sealed class DynamicView : MonoBehaviour
    {
        public Material[] materials;
        public Camera cameraView;
        public CrowdWorld world;
        Transform root;
        Transform[] movers,obstacles;
        public void Configure(CrowdWorld value)
        {
            if(root!=null){root.gameObject.SetActive(false);Destroy(root.gameObject);}
            world=value;root=new GameObject("Dynamic crowd world").transform;root.SetParent(transform);
            cameraView.transform.position=new Vector3(world.width/2f,65,world.height/2f);
            cameraView.transform.rotation=Quaternion.Euler(90,0,0);cameraView.orthographic=true;cameraView.orthographicSize=world.height*.62f;
            Shape("Floor",new Vector3(world.width/2f,-.15f,world.height/2f),new Vector3(world.width,.1f,world.height),0,false);
            obstacles=new Transform[world.width*world.height];
            for(int cell=0;cell<obstacles.Length;cell++)if(world.Solid(cell))obstacles[cell]=Obstacle(cell);
            for(int y=1;y<world.height-1;y++)
                Shape("Exit region",new Vector3(world.width-2,.05f,y),new Vector3(.9f,.05f,.9f),4,false);
            movers=new Transform[world.agents.Length];
            for(int i=0;i<movers.Length;i++)
                movers[i]=Shape("Disc "+i,Vector3.zero,new Vector3(CrowdWorld.Radius*2,.4f,CrowdWorld.Radius*2),2,false,PrimitiveType.Cylinder);
            Sync();
        }
        Transform Shape(string name,Vector3 position,Vector3 scale,int color,bool collider,PrimitiveType type=PrimitiveType.Cube)
        {
            var go=GameObject.CreatePrimitive(type);go.name=name;go.transform.SetParent(root);go.transform.position=position;go.transform.localScale=scale;
            go.GetComponent<Renderer>().sharedMaterial=materials[color];
            go.layer=collider?10:0;
            if(!collider){go.GetComponent<Collider>().enabled=false;Destroy(go.GetComponent<Collider>());}
            return go.transform;
        }
        Transform Obstacle(int cell)
        {var p=world.Center(cell);return Shape("Obstacle "+cell,new Vector3(p.x,.5f,p.y),new Vector3(1,1,1),1,true);}
        public void Sync()
        {
            for(int cell=0;cell<obstacles.Length;cell++)
            {
                bool solid=world.Solid(cell),pending=world.Pending(cell);
                if((solid||pending)&&obstacles[cell]==null)obstacles[cell]=Obstacle(cell);
                if(obstacles[cell]==null)continue;
                var go=obstacles[cell].gameObject;go.SetActive(solid||pending);
                var point=world.Center(cell);
                go.transform.position=new Vector3(point.x,pending?.05f:.5f,point.y);
                go.transform.localScale=pending?new Vector3(1,.05f,1):Vector3.one;
                go.GetComponent<Collider>().enabled=solid;
                go.GetComponent<Renderer>().sharedMaterial=materials[pending?5:1];
            }
            for(int i=0;i<movers.Length;i++)
            {var a=world.agents[i];movers[i].gameObject.SetActive(!a.arrived);movers[i].position=new Vector3(a.position.x,.5f,a.position.y);}
            Physics.SyncTransforms();
        }
        public int NativeWallOverlaps()
        {
            int hits=0;foreach(var a in world.agents)if(!a.arrived&&Physics.CheckSphere(new Vector3(a.position.x,.5f,a.position.y),CrowdWorld.Radius-.0001f,1<<10,QueryTriggerInteraction.Ignore))hits++;
            return hits;
        }
    }
}
