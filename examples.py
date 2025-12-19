"""
Example script demonstrating advanced MCMC usage for LVILC.

This example shows how to:
1. Load custom data
2. Use custom initial parameters
3. Run multiple chains with different settings
4. Analyze and compare results
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from lvilc_model import LVILCModel
from data_loader import CosmologyData
from mcmc_lvilc import LVILC_MCMC
from analysis import MCMCAnalyzer


def example_basic_mcmc():
    """
    Example 1: Basic MCMC run with default settings.
    """
    print("\n" + "="*70)
    print("Example 1: Basic MCMC Run")
    print("="*70)
    
    # Initialize data and MCMC
    data = CosmologyData()
    mcmc = LVILC_MCMC(data_loader=data)
    
    # Run MCMC with reduced steps for quick demonstration
    sampler = mcmc.run_mcmc(nwalkers=16, nsteps=1000, burn_in=200, progress=False)
    
    # Get and print results
    results = mcmc.get_results(sampler)
    
    print("\nResults:")
    for param in mcmc.param_names:
        print(f"{param}: {results[param]['median']:.3e} ± {results[param]['std']:.3e}")
    
    return results


def example_custom_initial_params():
    """
    Example 2: MCMC with custom initial parameters.
    """
    print("\n" + "="*70)
    print("Example 2: Custom Initial Parameters")
    print("="*70)
    
    # Try different initial values
    initial_params = np.array([-8.0, 5e23, 14.5])
    print(f"\nUsing initial parameters:")
    print(f"  H0 = {initial_params[0]} km/s/Mpc")
    print(f"  M_bh = {initial_params[1]:.2e} M_sun")
    print(f"  t_fall = {initial_params[2]} Gyr")
    
    data = CosmologyData()
    mcmc = LVILC_MCMC(data_loader=data)
    
    sampler = mcmc.run_mcmc(
        initial_params=initial_params,
        nwalkers=16,
        nsteps=1000,
        burn_in=200,
        progress=False
    )
    
    results = mcmc.get_results(sampler)
    
    print("\nResults:")
    for param in mcmc.param_names:
        print(f"{param}: {results[param]['median']:.3e} ± {results[param]['std']:.3e}")
    
    return results


def example_model_prediction():
    """
    Example 3: Make predictions with fitted model.
    """
    print("\n" + "="*70)
    print("Example 3: Model Predictions")
    print("="*70)
    
    # Use theoretical LVILC values
    H0 = -6.73
    M_bh = 1e23
    t_fall = 13.8
    
    model = LVILCModel(H0=H0, M_bh=M_bh, t_fall=t_fall)
    
    # Make predictions at different redshifts
    redshifts = [0.1, 0.5, 1.0, 1.5, 2.0]
    
    print("\nModel predictions:")
    print(f"{'z':<8} {'d_L (Mpc)':<15} {'μ':<10} {'H(z) (km/s/Mpc)':<20}")
    print("-" * 60)
    
    for z in redshifts:
        d_L = model.luminosity_distance(z)
        mu = model.distance_modulus(z)
        H_z = model.hubble_parameter(z)
        print(f"{z:<8.2f} {d_L:<15.2f} {mu:<10.2f} {H_z:<20.2f}")
    
    return model


def example_compare_models():
    """
    Example 4: Compare LVILC predictions with standard ΛCDM.
    """
    print("\n" + "="*70)
    print("Example 4: Model Comparison")
    print("="*70)
    
    # LVILC model
    lvilc_model = LVILCModel(H0=-6.73, M_bh=1e23, t_fall=13.8)
    
    # Simple ΛCDM approximation for comparison
    # (Using a simplified formula)
    def lcdm_distance_modulus(z, H0=70.0):
        """Simplified ΛCDM distance modulus."""
        # Approximate for flat ΛCDM with Ωm=0.3
        d_L = (3000 * z * (1 + z/2))  # Very approximate
        return 5 * np.log10(d_L) + 25
    
    # Compare at various redshifts
    z_range = np.linspace(0.1, 2.0, 20)
    
    lvilc_mu = [lvilc_model.distance_modulus(z) for z in z_range]
    lcdm_mu = [lcdm_distance_modulus(z) for z in z_range]
    
    print("\nDistance modulus comparison:")
    print(f"{'z':<8} {'LVILC μ':<12} {'ΛCDM μ':<12} {'Difference':<12}")
    print("-" * 50)
    
    for i in range(0, len(z_range), 4):
        z = z_range[i]
        diff = lvilc_mu[i] - lcdm_mu[i]
        print(f"{z:<8.2f} {lvilc_mu[i]:<12.2f} {lcdm_mu[i]:<12.2f} {diff:<12.2f}")
    
    # Create comparison plot
    plt.figure(figsize=(10, 6))
    plt.plot(z_range, lvilc_mu, 'r-', linewidth=2, label='LVILC')
    plt.plot(z_range, lcdm_mu, 'b--', linewidth=2, label='ΛCDM (approx.)')
    plt.xlabel('Redshift z', fontsize=12)
    plt.ylabel('Distance Modulus μ', fontsize=12)
    plt.title('LVILC vs ΛCDM Comparison', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(alpha=0.3)
    plt.savefig('model_comparison_example.png', dpi=300, bbox_inches='tight')
    print("\nComparison plot saved to: model_comparison_example.png")
    
    return lvilc_model


def example_parameter_sensitivity():
    """
    Example 5: Study parameter sensitivity.
    """
    print("\n" + "="*70)
    print("Example 5: Parameter Sensitivity Analysis")
    print("="*70)
    
    # Base model
    H0_base = -6.73
    M_bh_base = 1e23
    t_fall_base = 13.8
    
    z_test = 1.0
    
    # Vary H0
    print("\nSensitivity to H0 (at z=1.0):")
    H0_range = [-5.0, -6.73, -8.0, -10.0]
    for H0 in H0_range:
        model = LVILCModel(H0=H0, M_bh=M_bh_base, t_fall=t_fall_base)
        mu = model.distance_modulus(z_test)
        print(f"  H0 = {H0:6.2f} km/s/Mpc  →  μ = {mu:.3f}")
    
    # Vary M_bh
    print("\nSensitivity to M_bh (at z=1.0):")
    M_bh_range = [1e22, 1e23, 1e24, 1e25]
    for M_bh in M_bh_range:
        model = LVILCModel(H0=H0_base, M_bh=M_bh, t_fall=t_fall_base)
        mu = model.distance_modulus(z_test)
        print(f"  M_bh = {M_bh:.2e} M_sun  →  μ = {mu:.3f}")
    
    # Vary t_fall
    print("\nSensitivity to t_fall (at z=1.0):")
    t_fall_range = [12.0, 13.8, 15.0, 17.0]
    for t_fall in t_fall_range:
        model = LVILCModel(H0=H0_base, M_bh=M_bh_base, t_fall=t_fall)
        mu = model.distance_modulus(z_test)
        print(f"  t_fall = {t_fall:5.1f} Gyr  →  μ = {mu:.3f}")


if __name__ == '__main__':
    print("\n" + "="*70)
    print("LVILC MCMC Examples")
    print("="*70)
    
    # Run all examples
    try:
        example_basic_mcmc()
    except Exception as e:
        print(f"Example 1 error: {e}")
    
    try:
        example_custom_initial_params()
    except Exception as e:
        print(f"Example 2 error: {e}")
    
    try:
        example_model_prediction()
    except Exception as e:
        print(f"Example 3 error: {e}")
    
    try:
        example_compare_models()
    except Exception as e:
        print(f"Example 4 error: {e}")
    
    try:
        example_parameter_sensitivity()
    except Exception as e:
        print(f"Example 5 error: {e}")
    
    print("\n" + "="*70)
    print("All examples completed!")
    print("="*70 + "\n")
