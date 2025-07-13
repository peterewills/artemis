# Deterministic Drift Instability and Stochastic Thermal Perturbations of Magnetic Dissipative Droplet Solitons

**Authors:** P. Wills, E. Iacocca, and M. A. Hoefer (University of Colorado at Boulder & Chalmers University)

## Abstract

This paper quantifies the effects of thermal noise on magnetic dissipative droplets using soliton perturbation theory. The authors derive stochastic equations of motion for droplets and discover that deterministic droplets are linearly unstable at large bias currents, subject to a drift instability. The framework allows analytical computation of the droplet's generation linewidth and center variance.

## Main Contribution

The primary contribution is the development of a stochastic perturbation theory that:
1. Uncovers a previously unidentified deterministic drift instability at high bias currents
2. Provides analytical expressions for generation linewidth and droplet center variance
3. Explains low-frequency spectral features observed in experiments as drift instabilities

## Key Problem

Magnetic dissipative droplets are localized magnetic textures with potential applications in:
- Logic and storage technologies
- Communication applications
- Spin torque oscillators

The challenge is understanding how thermal noise affects droplet dynamics, particularly:
- Drift instabilities that cause droplets to exit the nanocontact region
- Random fluctuations vs. deterministic instabilities
- Generation linewidth broadening at room temperature

## Technical Approach

### Physical System

The droplets exist in:
- Magnetic thin films with perpendicular magnetic anisotropy (PMA)
- Nanocontact spin torque oscillators (NC-STOs)
- Systems where spin transfer torque (STT) balances magnetic damping

### Mathematical Framework

1. **Landau-Lifshitz Equation**: Governs magnetization dynamics with perturbations including:
   - Damping (α parameter)
   - Spin transfer torque (σ parameter)
   - Thermal random field (β parameter)

2. **Droplet Parameters**: Characterized by:
   - Center position (ξ)
   - Velocity (v)
   - Collective phase (φ)
   - Precessional frequency (ω)

3. **Perturbation Theory**: Valid for:
   - Large nanocontact radii (ρ* >> 1)
   - Weak damping/STT (σ = O(α) << 1)
   - Low temperature (β << 1)

### Key Innovation

The authors derive coupled stochastic differential equations for droplet parameters:
- Include higher-order corrections from soliton perturbation theory
- Model thermal noise as scaled Wiener processes with nontrivial covariance
- Linearize around stable fixed points to obtain analytical results

## Main Results

### 1. Deterministic Drift Instability

**Discovery**: Droplets become linearly unstable when:
```
αω*(2ω* + h₀) < (1/2)σω*(tanh((ρ* - 1)/ω*) + 1)
```

This condition was missed by previous analyses and shows that:
- High bias currents destabilize droplets
- The velocity eigenvalue λv can become positive
- Droplets drift away from the nanocontact region

### 2. Stochastic Analysis

For linearly stable droplets:

**Generation Linewidth**:
```
Δf = β²(ω*⁵/(4πλω²) + ω*/(2π))
```
- Linearly proportional to temperature
- Dominated by phase noise (Wiener process)
- Inversely proportional to nanocontact radius

**Droplet Center Variance**:
- Described by Ornstein-Uhlenbeck process
- STT acts as attractive mechanism keeping droplet centered
- Variance increases with temperature and decreases with nanocontact size

### 3. Parameter Regimes

The analysis identifies three regions in (h₀, σ/α) parameter space:
1. **No droplet existence** (σ < σmin)
2. **Linearly unstable** (high current regime)
3. **Stable droplet** (intermediate regime)

## Experimental Validation

### Numerical Simulations
- Nonlinear stochastic differential equations solved numerically
- Good agreement with linearized theory at low temperatures
- Linewidth enhancement at room temperature due to nonlinear effects

### Micromagnetic Simulations
- Include non-local dipole fields and Oersted fields
- Show qualitative agreement with analytical results
- Reveal that Oersted fields enhance linewidth by factor ~5

### Connection to Experiments
- Theory explains low-frequency spectral features as drift instabilities
- Typical experimental timescales allow many drift/renucleation events
- Small nanocontact devices more susceptible to drift instabilities

## Significance and Applications

### Theoretical Impact
1. First identification of deterministic drift instability mechanism
2. Analytical framework for understanding thermal effects on droplets
3. Explains discrepancies between theory and experiment

### Practical Implications
- Guides optimization of experimental parameters
- Suggests larger nanocontacts for improved stability
- Motivates temperature-dependent linewidth measurements
- Important for droplet-based device applications

## Key Insights

1. **Drift instabilities have dual origin**:
   - Deterministic (high current)
   - Stochastic (thermal fluctuations)

2. **Higher-order perturbation effects are essential**:
   - Phase dynamics include current-dependent corrections
   - Position dynamics coupled to velocity

3. **Room temperature operation challenges**:
   - Nonlinear effects enhance linewidth
   - Small basin of attraction for stable operation
   - Rare drift events become relevant on experimental timescales

## Conclusion

This work provides a complete theoretical framework for understanding magnetic droplet soliton dynamics under thermal perturbations. The discovery of deterministic drift instability and analytical expressions for key observables like linewidth advance both fundamental understanding and practical device optimization for droplet-based spintronics applications.