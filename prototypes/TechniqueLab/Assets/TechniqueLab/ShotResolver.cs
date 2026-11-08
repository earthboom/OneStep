using UnityEngine;

namespace TechniqueLab
{
    public struct ShotResult
    {
        public bool hitTarget, blocked;
        public Vector3 point;
        public string reason;
    }
    public static class ShotResolver
    {
        public static long QueryCount;
        public const int WallLayer = 8, TargetLayer = 9;
        public const int WorldMask = 1 << WallLayer;
        public const int AllMask = WorldMask | (1 << TargetLayer);
        public static ShotResult CameraOnly(Vector3 camera, Vector3 direction, float range)
        {
            RaycastHit hit; QueryCount++;
            bool found = Physics.Raycast(camera, direction, out hit, range, AllMask, QueryTriggerInteraction.Ignore);
            return new ShotResult { hitTarget = found && hit.collider.gameObject.layer == TargetLayer,
                blocked = found && hit.collider.gameObject.layer == WallLayer,
                point = found ? hit.point : camera + direction.normalized * range, reason = "camera-only" };
        }
        public static ShotResult Resolve(Vector3 camera, Vector3 direction, Vector3 root, Vector3 muzzle, float range)
        {
            var intent=CameraOnly(camera,direction,range); RaycastHit hit;
            QueryCount++;
            if(Physics.CheckSphere(muzzle,0.025f,WorldMask,QueryTriggerInteraction.Ignore))
                return new ShotResult{blocked=true,point=muzzle,reason="muzzle-overlap"};
            QueryCount++;
            if(Physics.CheckSphere(root,0.025f,WorldMask,QueryTriggerInteraction.Ignore))
                return new ShotResult{blocked=true,point=root,reason="root-overlap"};
            var toMuzzle=muzzle-root;
            if(toMuzzle.sqrMagnitude>0.000001f)
            {
                QueryCount++;
                if(Physics.Raycast(root,toMuzzle.normalized,out hit,toMuzzle.magnitude,WorldMask,QueryTriggerInteraction.Ignore))
                    return new ShotResult{blocked=true,point=hit.point,reason="root-obstruction"};
            }
            var delta=intent.point-muzzle;
            if(delta.sqrMagnitude<0.000001f)return new ShotResult{point=muzzle,reason="zero-length"};
            QueryCount++;
            bool found=Physics.Raycast(muzzle,delta.normalized,out hit,Mathf.Min(range,delta.magnitude+0.001f),AllMask,QueryTriggerInteraction.Ignore);
            return new ShotResult{hitTarget=found&&hit.collider.gameObject.layer==TargetLayer,
                blocked=found&&hit.collider.gameObject.layer==WallLayer,
                point=found?hit.point:intent.point,reason=found?"muzzle-first-hit":"miss"};
        }
    }
}
