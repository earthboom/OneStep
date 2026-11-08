using UnityEngine;

namespace TechniqueLab
{
    public sealed class LabView : MonoBehaviour
    {
        public Material[] materials;
        public Font font;
        public Camera displayCamera;
        public WeightedGraph graph;
        public WeightedField field;
        public int CoverState {get;private set;}
        public bool DoorClosed {get;private set;}
        public readonly Vector3 shotBase=new Vector3(9,0,9);
        public Vector3 ShotCamera {get{return shotBase+new Vector3(0,2,-6);}}
        public Vector3 Muzzle {get{return shotBase+new Vector3(1,1,-3);}}
        public Vector3 WeaponRoot {get{return shotBase+new Vector3(0,1,-3);}}
        public Vector3 ShotDirection {get{return (shotBase+new Vector3(0,1,8)-ShotCamera).normalized;}}
        public ShotResult nativeShot;
        public bool cameraOnlyHit;
        Transform target,naive,correct,wall,rayIntent,rayMuzzle,door;
        Transform[] agents;int[] cells;
        float naiveX,correctX;

        Transform Shape(string name,Vector3 position,Vector3 size,int color,int layer=0,bool collider=false)
        {
            var go=GameObject.CreatePrimitive(PrimitiveType.Cube);go.name=name;go.transform.SetParent(transform);
            go.transform.position=position;go.transform.localScale=size;go.layer=layer;
            go.GetComponent<Renderer>().sharedMaterial=materials[color];
            if(!collider){var c=go.GetComponent<Collider>();c.enabled=false;Destroy(c);}
            return go.transform;
        }
        void Label(string text,Vector3 position)
        {
            var go=new GameObject(text);go.transform.SetParent(transform);go.transform.position=position;
            go.transform.rotation=displayCamera.transform.rotation;
            var mesh=go.AddComponent<TextMesh>();mesh.text=text;mesh.font=font;mesh.fontSize=64;
            mesh.characterSize=0.13f;mesh.anchor=TextAnchor.MiddleCenter;mesh.color=Color.white;
            go.GetComponent<MeshRenderer>().sharedMaterial=font.material;
        }
        public void Build()
        {
            Shape("Floor",new Vector3(0,-0.2f,5),new Vector3(40,0.2f,34),0);
            Label("FRAME-RATE RESPONSE",new Vector3(-6,1,-9));
            Label("TARGET / FRAME LERP / EXP DAMPING",new Vector3(-6,0.8f,-7.8f));
            target=Shape("Camera target",new Vector3(-8,0.5f,-5),Vector3.one,2);
            naive=Shape("Per-frame follower",new Vector3(-8,0.5f,-3.5f),Vector3.one,3);
            correct=Shape("Time-consistent follower",new Vector3(-8,0.5f,-2),Vector3.one,4);
            ResetCamera();
            Label("NATIVE PHYSICS COVER",new Vector3(9,1,0));
            Shape("Aim camera",ShotCamera,Vector3.one*0.4f,2);
            Shape("Weapon root",WeaponRoot,Vector3.one*0.3f,5);
            Shape("Muzzle",Muzzle,Vector3.one*0.35f,3);
            Shape("Target",shotBase+new Vector3(0,1,8),new Vector3(1,2,1),4,ShotResolver.TargetLayer,true);
            wall=Shape("Offset cover",shotBase+new Vector3(1,1,-1),new Vector3(0.7f,2,0.4f),1,ShotResolver.WallLayer,true);
            rayIntent=Shape("Camera intention ray",Vector3.zero,Vector3.one,2);
            rayMuzzle=Shape("Muzzle resolved ray",Vector3.zero,Vector3.one,3);
            Label("SHARED WEIGHTED EXIT FIELD",new Vector3(-8,1,21));
            graph=WeightedGraph.Grid(32);field=new WeightedField(graph.Count);field.Compute(graph,graph.Count-1);
            for(int i=0;i<graph.Count;i++)if(graph.blocked[i])Shape("Grid wall",GridPosition(i),new Vector3(.43f,.7f,.43f),1);
            door=Shape("Dynamic door",GridPosition(16*32+16),new Vector3(.43f,.8f,.43f),3);door.gameObject.SetActive(false);
            Shape("Exit",GridPosition(graph.Count-1),new Vector3(.65f,.4f,.65f),4);
            agents=new Transform[64];cells=new int[64];
            for(int i=0;i<agents.Length;i++)
            {cells[i]=(i*47)%graph.Count;while(graph.blocked[cells[i]])cells[i]=(cells[i]+1)%graph.Count;
                agents[i]=Shape("Route consumer "+i,GridPosition(cells[i])+Vector3.up*.45f,Vector3.one*.17f,5);}
            Physics.SyncTransforms();RefreshShot();
        }
        Vector3 GridPosition(int node){return new Vector3(-16+(node%32)*.45f,.2f,4+(node/32)*.45f);}
        static void Line(Transform line,Vector3 a,Vector3 b)
        {var d=b-a;line.position=(a+b)*.5f;line.rotation=d.sqrMagnitude>0?Quaternion.LookRotation(d):Quaternion.identity;line.localScale=new Vector3(.055f,.055f,Mathf.Max(.01f,d.magnitude));}
        public void ResetCamera(){naiveX=correctX=-8;}
        public void SetCover(int state)
        {
            CoverState=state;wall.position=shotBase+(state==0?new Vector3(1,1,-1):state==1?new Vector3(5,1,-1):new Vector3(1,1,-3));
            Physics.SyncTransforms();RefreshShot();
        }
        public void CycleCover(){SetCover((CoverState+1)%3);}
        public void ToggleDoor()
        {
            DoorClosed=!DoorClosed;graph.SetBlocked(16*32+16,DoorClosed);field.Compute(graph,graph.Count-1);door.gameObject.SetActive(DoorClosed);
            // This routing illustration resets movers at a topology change; it does not solve in-flight collision reconciliation.
            for(int i=0;i<agents.Length;i++){cells[i]=i%16;agents[i].position=GridPosition(cells[i])+Vector3.up*.45f;}
        }
        public void RefreshShot()
        {
            var intent=ShotResolver.CameraOnly(ShotCamera,ShotDirection,50);cameraOnlyHit=intent.hitTarget;
            nativeShot=ShotResolver.Resolve(ShotCamera,ShotDirection,WeaponRoot,Muzzle,50);
            Line(rayIntent,ShotCamera,intent.point);Line(rayMuzzle,Muzzle,nativeShot.point);
        }
        void Update()
        {
            float dt=Time.unscaledDeltaTime;float x=-8+5*Mathf.Sin(Time.unscaledTime*.8f);
            target.position=new Vector3(x,.5f,-5);naiveX=Mathf.Lerp(naiveX,x,.1f);correctX=CameraDamping.Step(correctX,x,4,dt);
            naive.position=new Vector3(naiveX,.5f,-3.5f);correct.position=new Vector3(correctX,.5f,-2);
            if(!field.IsValidFor(graph))throw new System.InvalidOperationException("Visual consumer saw a stale field");
            for(int i=0;i<agents.Length;i++)
            {
                int node=cells[i];if(node==graph.Count-1){cells[i]=i%16;agents[i].position=GridPosition(cells[i])+Vector3.up*.45f;continue;}
                int next=field.Next(graph,node);if(next<0)continue;
                if(graph.blocked[next])throw new System.InvalidOperationException("Route enters blocked cell");
                Vector3 destination=GridPosition(next)+Vector3.up*.45f;
                agents[i].position=Vector3.MoveTowards(agents[i].position,destination,2*dt);
                if((agents[i].position-destination).sqrMagnitude<.00001f)cells[i]=next;
            }
        }
    }
}
