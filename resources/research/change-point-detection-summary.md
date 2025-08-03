# Change Point Detection in a Dynamic Stochastic Blockmodel

**Authors:** Peter Wills and François G. Meyer (University of Colorado at Boulder)

## Abstract

This paper develops a statistical test to detect when communities in a growing network are merging, without needing to first identify what the communities are. The authors study a dynamic version of the stochastic blockmodel where new vertices are continuously added to an existing two-community network.

## Main Contribution

The primary contribution is a rigorous analysis of a dynamic community graph model that can detect structural changes between communities while remaining robust to random fluctuations within communities. The method circumvents the computationally challenging problem of community detection by using a global metric based on network resistance.

## Key Problem

Social networks and other real-world networks exhibit community structure and undergo significant structural changes over time, such as:
- Communities merging
- New hubs emerging between disparate regions
- Structural disruptions due to external events

The challenge is detecting these meaningful structural changes while distinguishing them from random fluctuations in connectivity.

## Technical Approach

### Dynamic Stochastic Blockmodel

The authors define a growing network model where:
- Start with a two-community stochastic blockmodel
- At each time step, add a new vertex assigned to one of the communities
- Connect it randomly to existing vertices with probabilities:
  - `p_n` (within community connections)
  - `q_n` (between community connections)

### Test Statistic

The method uses the **resistance perturbation distance** (`d_rp`), which:
- Measures changes in effective resistance between vertices as the network evolves
- Is sensitive to global connectivity changes between communities
- Remains relatively robust to local changes within communities
- Can be computed efficiently (linear in the number of edges)

### Hypothesis Testing

The test statistic `Z_n` distinguishes between:
- **Null hypothesis**: No new cross-community edges added (`k_{n+1} = k_n`)
- **Alternative hypothesis**: New cross-community edges added (`k_{n+1} > k_n`)

## Main Theoretical Result

**Theorem 1** establishes that the expected value of the test statistic `E[Z_n]` is:

- **Under null hypothesis**: `O(1/√d_n)`
- **Under alternative hypothesis**: `2p_n/(n²q_n²) + O(1/√d_n)`

### Key Conditions

The test works effectively when:
- `p_n = ω(log n/n)` (within-community edge probability)
- `p_n/n < q_n < (p_n/n)^(3/4)` (cross-community edge probability constraint)

This ensures that cross-community changes aren't masked by within-community noise.

## Experimental Validation

### Synthetic Data
- Monte Carlo simulations with 64 random realizations
- Graph size: n = 2,048 vertices
- Edge density: `p_n = log²(n)/n`
- Results confirm theoretical predictions across various parameter ranges

### Real-World Data: Primary School Network
- **Dataset**: Face-to-face contact network from RFID tags in a primary school
- **Structure**: 232 students across 10 classes (5 grades × 2 classes each)
- **Events**: Lunch periods and recess times cause structural changes
- **Results**: Method successfully detects community structure changes during events while remaining robust to random fluctuations

### Comparison with Other Methods
The resistance perturbation distance outperformed:
- DeltaCon distance
- NetSimile distance
- Edit distance
- Spectral distances (combinatorial Laplacian, normalized Laplacian, adjacency)

## Significance and Applications

### Advantages
1. **No community detection required**: Detects structural changes without first identifying communities
2. **Computationally efficient**: Linear complexity in number of edges
3. **Streaming capability**: Can be updated incrementally as networks grow
4. **Robust to noise**: Distinguishes meaningful structural changes from random fluctuations

### Practical Applications
- Social network monitoring
- Infrastructure network analysis
- Biological network evolution
- Real-time anomaly detection in dynamic networks

## Technical Innovation

The key insight is using **effective resistance** from electrical network theory to measure network connectivity. This provides a principled way to:
- Quantify how adding edges affects global network structure
- Distinguish between local (within-community) and global (between-community) changes
- Create a sensitive yet robust change detection method

## Future Extensions

The authors note several promising directions:
- Extension to fixed-size networks with edge addition/deletion
- Multi-community scenarios (demonstrated with 10-community school network)
- Latent process modeling for edge dynamics
- Streaming graph applications

## Conclusion

This work provides a theoretically grounded and practically useful method for detecting community-level structural changes in growing networks. By leveraging resistance perturbation distance, it offers a computationally efficient solution that's sensitive to meaningful changes while robust to noise - making it valuable for real-world network monitoring applications.