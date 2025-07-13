# Performance of Test Supermartingale Confidence Intervals for the Success Probability of Bernoulli Trials

**Authors:** Peter Wills (CU Boulder), Emanuel Knill (NIST & CU Boulder), Kevin Coakley (NIST), and Yanbao Zhang (University of Waterloo & NTT)

## Abstract

This paper compares test supermartingales to traditional methods for computing p-values and confidence intervals in Bernoulli trials. Test supermartingales are valuable for obtaining extremely small p-values and remain valid under arbitrary stopping rules. The study quantifies the performance cost of this robustness by comparing to Chernoff-Hoeffding bounds and exact p-value calculations.

## Main Contribution

The primary contributions are:
1. Systematic comparison of test supermartingales with exact tests and Chernoff-Hoeffding bounds
2. Quantification of the "cost" of stopping-rule robustness in terms of p-value and confidence interval performance
3. Demonstration that confidence intervals from test supermartingales grow as Ω(√log(n)) rather than O(1)
4. Showing that despite systematic gaps, test supermartingales perform well relative to experiment-to-experiment variation

## Key Problem

**Motivation from Physics:**
- Bell test experiments require extremely high confidence (very small p-values)
- Need to reject local realist theories and certify quantum entanglement
- Traditional methods fail due to non-i.i.d. trials and Gaussian approximation breakdown in extreme tails
- Applications in randomness certification require p-values as small as 10^(-100) or smaller

**General Challenge:**
- Need valid statistical inference with arbitrary stopping rules
- Must handle adaptive experiments and dependent trials
- Traditional methods require fixed sample sizes or independence assumptions

## Technical Approach

### Test Supermartingales

A test supermartingale T = (Ti) for null hypothesis H₀ satisfies:
- T₀ = 1 (initial value)
- Ti ≥ 0 (non-negative)
- E(Ti+1|past) ≤ Ti (supermartingale property under H₀)

**Key Properties:**
- p-value given by P = 1/Tn (by Markov's inequality)
- Valid under arbitrary stopping rules
- Can be constructed adaptively during experiment

### Probability-Based Ratio (PBR) Method

Constructs test factors Fi = Ti/Ti-1 adaptively:
1. Estimate distribution from past trials
2. Find closest distribution in null hypothesis (KL divergence)
3. Set test factor as ratio of estimated to null distribution

### Comparison Framework

Three methods compared for Bernoulli trials with success probability θ:
1. **Exact test (PX)**: Uses binomial tail probabilities
2. **Chernoff-Hoeffding (PCH)**: Optimal large deviation bound
3. **PBR test (PPBR)**: Test supermartingale method

## Main Results

### 1. P-Value Comparison

**Theorem 1**: Ordering of p-values
```
PX ≤ PCH ≤ PPBR
```

**Theorem 2**: Systematic gaps between log(p)-values
```
-log(PPBR) = -log(PCH) - (1/2)log(n+1) + O(1)
-log(PX) = -log(PCH) + (1/2)log(n) + O(1)
```

Key insight: Test supermartingales lose a factor of approximately √n in p-value

### 2. Asymptotic Behavior

**Theorem 3**: All three methods achieve asymptotically optimal rates
```
√n(-log(P)/n - KL(θ|φ)) → N(0, σ²)
```
where KL is Kullback-Leibler divergence and σ² depends on parameters.

**Implication**: Despite systematic gaps, variation between experiments dominates the differences between methods.

### 3. Confidence Intervals

For confidence intervals at level α:

**Standard methods**: Interval width scales as O(1/√n)

**Test supermartingales**: Normalized endpoint deviation is Ω(√log(n))
- This represents the cost of stopping-rule robustness
- Related to law of iterated logarithm
- Can be reduced to O(1) if n is fixed in advance with adaptive construction

## Practical Implications

### When to Use Test Supermartingales

**Advantages:**
- Arbitrary stopping rules allowed
- Adaptive construction during experiment
- Valid for non-i.i.d. sequences
- Extremely small p-values remain rigorous

**Disadvantages:**
- Systematically larger p-values (factor ~√n)
- Wider confidence intervals (factor ~√log(n))
- More complex to implement

### Applications

**Ideal for:**
- Bell test experiments
- Quantum randomness certification
- Sequential testing with optional stopping
- Adaptive experiments with changing parameters

**Less suitable for:**
- Fixed sample size experiments
- When tightest possible bounds needed
- Simple i.i.d. settings

## Technical Innovation

### Adaptive Testing

The PBR method demonstrates how adaptivity helps:
- Can recalibrate during experiment
- Automatically ignores periods where null holds
- Focuses on periods providing evidence against null

### Extended Nulls

Test supermartingales naturally handle extended nulls where:
- Parameters can vary between trials
- Dependencies on past outcomes allowed
- Only requirement: each trial satisfies null constraint

## Significance

### Theoretical Impact
- Rigorous framework for extreme p-values
- Quantifies cost of robustness
- Connects martingale theory to practical testing

### Practical Applications
- Enables valid Bell test analysis
- Supports quantum information protocols
- Allows flexible experimental designs

## Future Directions

The authors note several extensions:
- Optimal test supermartingale construction
- Reducing confidence interval width when n known
- Applications beyond Bernoulli trials
- Integration with other quantum protocols

## Conclusion

Test supermartingales provide a powerful framework for hypothesis testing with extreme requirements on significance levels and experimental flexibility. While they incur a systematic cost compared to traditional methods, this cost is often negligible compared to experimental variation and is outweighed by the benefits of stopping-rule robustness and adaptivity. The methods are particularly valuable for quantum experiments and other settings requiring both extreme confidence and experimental flexibility.