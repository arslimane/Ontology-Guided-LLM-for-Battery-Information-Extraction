#!/usr/bin/env python3
"""Verify CUDA and PyTorch installation."""

import sys


def check_cuda_setup():
    """Check CUDA and PyTorch configuration."""
    print("=" * 60)
    print("CUDA & PyTorch Environment Check")
    print("=" * 60)

    # Check Python version
    print(f"\n✓ Python version: {sys.version.split()[0]}")

    # Try to import torch
    try:
        import torch

        print(f"✓ PyTorch version: {torch.__version__}")
    except ImportError:
        print("✗ PyTorch not installed!")
        print("\n  Run one of:")
        print("    ./setup-cuda.sh setup   (for CUDA 13.0)")
        return False

    # Check CUDA availability
    cuda_available = torch.cuda.is_available()
    print(f"{'✓' if cuda_available else '✗'} CUDA available: {cuda_available}")

    if cuda_available:
        print(f"✓ CUDA version: {torch.version.cuda}")
        print(f"✓ cuDNN version: {torch.backends.cudnn.version()}")
        print(f"✓ Number of GPUs: {torch.cuda.device_count()}")

        for i in range(torch.cuda.device_count()):
            props = torch.cuda.get_device_properties(i)
            print(f"\n  GPU {i}: {props.name}")
            print(f"    Memory: {props.total_memory / 1024**3:.2f} GiB")
            print(f"    Compute Capability: {props.major}.{props.minor}")
            print(
                f"    Current Memory Usage: {torch.cuda.memory_allocated(i) / 1024**3:.2f} GiB"
            )
    else:
        print("\n⚠ CUDA not available. Possible reasons:")
        print("  - No GPU detected")
        print("  - Wrong PyTorch CUDA version for your driver")
        print("  - GPU drivers not installed")
        print("\n  Check driver version with: nvidia-smi")
    # Check other key packages
    print("\n" + "=" * 60)
    print("Key Packages")
    print("=" * 60)

    packages_to_check = [
        "transformers",
        "accelerate",
        "bitsandbytes",
        "numpy",
        "pandas",
    ]

    for package_name in packages_to_check:
        try:
            module = __import__(package_name)
            version = getattr(module, "__version__", "unknown")
            print(f"✓ {package_name}: {version}")
        except ImportError:
            print(f"✗ {package_name}: not installed")

    # Check flash-attn separately (optional)
    try:
        import flash_attn

        print(f"✓ flash-attn: {flash_attn.__version__} (optional)")
    except ImportError:
        print("  flash-attn: not installed ")

    print("\n" + "=" * 60)

    # Read current CUDA config
    try:
        with open(".cuda-config", "r") as f:
            config = f.read().strip().split("\n")[-1]
            print(f"Current config marker: {config}")
    except FileNotFoundError:
        print("No .cuda-config found")

    print("=" * 60)

    return cuda_available


if __name__ == "__main__":
    success = check_cuda_setup()
    sys.exit(0 if success else 1)
 