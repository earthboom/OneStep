using UnityEngine;

namespace WorldLifecycle
{
    public sealed class WolfView : MonoBehaviour
    {
        internal WolfState PresentedState { get; private set; }

        internal void Present(WolfState state)
        {
            PresentedState = state;
            float angle = (state.PatrolSteps % 8) * (360f / 8f);
            transform.position = new Vector3(WorldLifecycleGame.ForestX, 0, 0) +
                Quaternion.Euler(0, angle, 0) * Vector3.forward * 3.2f;
            transform.rotation = state.Hp == 0 ? Quaternion.Euler(0, angle, 90) : Quaternion.Euler(0, angle, 0);
        }
    }
}
