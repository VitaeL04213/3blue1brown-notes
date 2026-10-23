import Mathlib

namespace ThreeBlueOneBrown.Lockdown

theorem quadratic_centering (x m p : ℝ) :
    x^2-2*m*x+p=(x-m)^2-(m^2-p) := by ring

theorem unit_circle (θ : ℝ) : Real.sin θ^2+Real.cos θ^2=1 :=
  Real.sin_sq_add_cos_sq θ

theorem complex_square_i : Complex.I^2 = -1 := Complex.I_sq

theorem exponential_add (z w : ℂ) :
    Complex.exp (z+w)=Complex.exp z*Complex.exp w := Complex.exp_add z w

theorem imaginary_step_norm (h : ℝ) :
    Complex.normSq (1+(h:ℂ)*Complex.I)=1+h^2 := by
  simp [Complex.normSq_apply, pow_two]

theorem logarithm_product (a b : ℝ) (ha : 0<a) (hb : 0<b) :
    Real.log (a*b)=Real.log a+Real.log b := Real.log_mul (ne_of_gt ha) (ne_of_gt hb)

theorem natural_log_derivative (x : ℝ) (hx : 0<x) :
    HasDerivAt Real.log (1/x) x := by
  simpa [one_div] using Real.hasDerivAt_log (ne_of_gt hx)

-- Necessary fixed-point equation conditional on convergence, not a convergence proof.
theorem tower_limit_fixed_point (f : ℝ → ℝ) (u : ℕ → ℝ) (L : ℝ)
    (hc : ContinuousAt f L) (hu : Filter.Tendsto u Filter.atTop (nhds L))
    (hs : ∀ n, u (n+1)=f (u n)) : f L=L := by
  have hshift : Filter.Tendsto (fun n => u (n+1)) Filter.atTop (nhds L) :=
    hu.comp (Filter.tendsto_add_atTop_nat 1)
  have hfun : (fun n => f (u n)) = fun n => u (n+1) := by
    funext n
    exact (hs n).symm
  have hf := hc.tendsto.comp hu
  change Filter.Tendsto (fun n => f (u n)) _ _ at hf
  rw [hfun] at hf
  exact tendsto_nhds_unique hf hshift

theorem i_log_branch_exponent (θ : ℝ) :
    Complex.I*((θ:ℂ)*Complex.I)=-(θ:ℂ) := by
  calc
    Complex.I*((θ:ℂ)*Complex.I) = (θ:ℂ)*(Complex.I*Complex.I) := by ring
    _ = -(θ:ℂ) := by simp

theorem symmetric_problem_reduction (x y : ℝ) :
    x^2+y^2=(x+y)^2-2*x*y := by ring

end ThreeBlueOneBrown.Lockdown
