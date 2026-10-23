import Mathlib

namespace ThreeBlueOneBrown.DifferentialEquations

theorem exponential_solution (k t : ℝ) :
    HasDerivAt (fun s : ℝ => Real.exp (k*s)) (k*Real.exp (k*t)) t := by
  convert (Real.hasDerivAt_exp (k*t)).comp t ((hasDerivAt_id t).const_mul k) using 1
  ring

theorem heat_stencil (a b c d e f κ : ℝ) :
    κ*((a+d)-2*(b+e)+(c+f)) = κ*(a-2*b+c)+κ*(d-2*e+f) := by ring

theorem heat_mode_decay (κ n t : ℝ) :
    HasDerivAt (fun s : ℝ => Real.exp (-κ*n^2*s))
      (-κ*n^2*Real.exp (-κ*n^2*t)) t := exponential_solution (-κ*n^2) t

theorem fourier_superposition (a b : ℂ) (θ : ℝ) :
    (a+b)*Complex.exp ((θ:ℂ)*Complex.I) =
      a*Complex.exp ((θ:ℂ)*Complex.I)+b*Complex.exp ((θ:ℂ)*Complex.I) := by ring

theorem rotating_exponential_norm (θ : ℝ) :
    ‖Complex.exp ((θ:ℂ)*Complex.I)‖ = 1 := Complex.norm_exp_ofReal_mul_I θ

theorem laplace_kernel (s a t : ℝ) :
    Real.exp (-s*t)*Real.exp (a*t)=Real.exp (-(s-a)*t) := by
  rw [← Real.exp_add]
  congr 1
  ring

theorem transformed_oscillator (s ω Y F y₀ v₀ : ℝ)
    (h : s^2*Y-s*y₀-v₀+ω^2*Y=F) (hn : s^2+ω^2 ≠ 0) :
    Y=(F+s*y₀+v₀)/(s^2+ω^2) := by
  apply (eq_div_iff hn).2
  nlinarith

theorem euler_identity : Complex.exp ((Real.pi:ℂ)*Complex.I) = -1 := by
  exact Complex.exp_pi_mul_I

theorem nilpotent_exponential_add (A : Matrix (Fin 2) (Fin 2) ℝ)
    (hA : A*A=0) (s t : ℝ) :
    (1+s • A)*(1+t • A)=1+(s+t) • A := by
  simp [add_mul, mul_add, Matrix.smul_mul, Matrix.mul_smul, hA, add_smul]
  abel

theorem logistic_threshold (r K N : ℝ) (hr : 0 < r) (hK : 0 < K)
    (hN : 0 < N) (hNK : N < K) : 0 < r*N*(1-N/K) := by
  apply mul_pos (mul_pos hr hN)
  have : N/K < 1 := (div_lt_one hK).2 hNK
  linarith

end ThreeBlueOneBrown.DifferentialEquations
