import Mathlib

namespace ThreeBlueOneBrown.Calculus
open Filter
open scoped Topology

theorem area_derivative (x : ℝ) :
    HasDerivAt (fun t : ℝ => t^2/2) x x := by
  convert (hasDerivAt_pow 2 x).div_const 2 using 1
  ring

theorem square_secant (x h : ℝ) (hh : h ≠ 0) :
    ((x+h)^2-x^2)/h = 2*x+h := by field_simp; ring

theorem power_rule (n : ℕ) (x : ℝ) :
    HasDerivAt (fun t : ℝ => t^n) ((n:ℝ)*x^(n-1)) x := hasDerivAt_pow n x

theorem sine_derivative (x : ℝ) : HasDerivAt Real.sin (Real.cos x) x :=
  Real.hasDerivAt_sin x

theorem product_rule (f g : ℝ → ℝ) (x df dg : ℝ)
    (hf : HasDerivAt f df x) (hg : HasDerivAt g dg x) :
    HasDerivAt (fun t => f t*g t) (df*g x+f x*dg) x := hf.mul hg

theorem chain_rule (f g : ℝ → ℝ) (x df dg : ℝ)
    (hf : HasDerivAt f df x) (hg : HasDerivAt g dg (f x)) :
    HasDerivAt (fun t => g (f t)) (dg*df) x := hg.comp x hf

theorem exponential_derivative (x : ℝ) : HasDerivAt Real.exp (Real.exp x) x :=
  Real.hasDerivAt_exp x

theorem circle_tangent (x y dx dy : ℝ) (hy : y ≠ 0)
    (h : 2*x*dx+2*y*dy=0) : dy= -x*dx/y := by
  apply (eq_div_iff hy).2
  nlinarith

theorem square_limit (a : ℝ) :
    Tendsto (fun x : ℝ => x^2) (𝓝 a) (𝓝 (a^2)) :=
  (continuous_pow 2).continuousAt.tendsto

theorem epsilon_delta_linear (a ε : ℝ) (hε : 0 < ε) :
    ∃ δ : ℝ, 0 < δ ∧ ∀ x : ℝ, |x-a| < δ → |(3*x+2)-(3*a+2)| < ε := by
  refine ⟨ε/3, by positivity, ?_⟩
  intro x hx
  have heq : (3*x+2)-(3*a+2)=3*(x-a) := by ring
  rw [heq, abs_mul, abs_of_pos (by norm_num : (0:ℝ)<3)]
  linarith

-- A concrete removable-singularity limit, not the full general l'Hopital theorem.
theorem removable_limit :
    Tendsto (fun x : ℝ => (x^2-1)/(x-1)) (𝓝[≠] 1) (𝓝 2) := by
  have h : (fun x : ℝ => (x^2-1)/(x-1)) =ᶠ[𝓝[≠] 1] (fun x => x+1) := by
    filter_upwards [self_mem_nhdsWithin] with x hx
    have hn : x-1 ≠ 0 := sub_ne_zero.mpr hx
    field_simp
    ring
  apply Tendsto.congr' h.symm
  have hc : ContinuousAt (fun x : ℝ => x+1) 1 := by fun_prop
  have hlim : Tendsto (fun x : ℝ => x+1) (𝓝[≠] (1:ℝ)) (𝓝 ((1:ℝ)+1)) :=
    hc.tendsto.mono_left nhdsWithin_le_nhds
  norm_num at hlim
  exact hlim

theorem fundamental_theorem (f : ℝ → ℝ) (a b : ℝ)
    (hd : ∀ x ∈ Set.uIcc a b, DifferentiableAt ℝ f x)
    (hi : IntervalIntegrable (deriv f) MeasureTheory.volume a b) :
    (∫ x in a..b, deriv f x) = f b-f a :=
  intervalIntegral.integral_deriv_eq_sub hd hi

theorem triangle_area (a : ℝ) : (∫ x in (0:ℝ)..a, x) = a^2/2 := by
  simp [integral_id]

theorem second_derivative_cubic (x : ℝ) :
    deriv (deriv (fun t : ℝ => t^3)) x = 6*x := by
  have h : deriv (fun t : ℝ => t^3) = fun t => 3*t^2 := by
    funext t
    simp [deriv_pow]
  rw [h]
  convert ((hasDerivAt_pow 2 x).const_mul 3).deriv using 1
  ring

theorem cubic_taylor_exact (a h : ℝ) :
    (a+h)^3=a^3+3*a^2*h+3*a*h^2+h^3 := by ring

theorem quadratic_error (a h : ℝ) : (a+h)^2-a^2-2*a*h=h^2 := by ring

theorem derivative_composition_scale (a b x : ℝ) :
    HasDerivAt (fun t : ℝ => a*(b*t)) (a*b) x := by
  simpa using ((hasDerivAt_id x).const_mul b).const_mul a

theorem planar_divergence (a b : ℝ) :
    deriv (fun x : ℝ => a*x) 0 + deriv (fun y : ℝ => b*y) 0 = a+b := by
  have ha : deriv (fun x : ℝ => a*x) 0 = a := by
    simpa using ((hasDerivAt_id (0:ℝ)).const_mul a).deriv
  have hb : deriv (fun x : ℝ => b*x) 0 = b := by
    simpa using ((hasDerivAt_id (0:ℝ)).const_mul b).deriv
  rw [ha, hb]

end ThreeBlueOneBrown.Calculus
