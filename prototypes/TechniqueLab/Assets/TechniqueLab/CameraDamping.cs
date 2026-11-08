using UnityEngine;

namespace TechniqueLab
{
    public static class CameraDamping
    {
        public static float Alpha(float rate, float dt) { return 1f-Mathf.Exp(-rate*dt); }
        public static float Step(float current, float target, float rate, float dt)
        { return Mathf.LerpUnclamped(current, target, Alpha(rate, dt)); }
        public static Vector3 Step(Vector3 current, Vector3 target, float rate, float dt)
        { return Vector3.LerpUnclamped(current, target, Alpha(rate, dt)); }
    }
}
