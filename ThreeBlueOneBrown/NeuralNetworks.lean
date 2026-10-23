import Mathlib

namespace ThreeBlueOneBrown.NeuralNetworks

theorem affine_composition (a b c d x : ℝ) :
    a*(b*x+c)+d = (a*b)*x+(a*c+d) := by ring

theorem quadratic_gradient_step (x η : ℝ) (h₀ : 0 ≤ η) (h₁ : η ≤ 1) :
    (x-η*(2*x))^2 ≤ x^2 := by
  have h : (1-2*η)^2 ≤ (1:ℝ) := by nlinarith
  have hm := mul_le_mul_of_nonneg_right h (sq_nonneg x)
  nlinarith

theorem affine_input_sensitivity (w b x δ : ℝ) :
    (w*(x+δ)+b)-(w*x+b)=w*δ := by ring

theorem gradient_accumulation (f g : ℝ → ℝ) (x df dg : ℝ)
    (hf : HasDerivAt f df x) (hg : HasDerivAt g dg x) :
    HasDerivAt (fun t => f t+g t) (df+dg) x := hf.add hg

theorem squared_loss_weight_gradient (a b y w : ℝ) :
    HasDerivAt (fun t : ℝ => (t*a+b-y)^2) (2*(w*a+b-y)*a) w := by
  convert ((((hasDerivAt_id w).mul_const a).add_const b).sub_const y).pow 2 using 1
  simp only [id_eq]
  ring

theorem conditional_product_bounds (p q : ℝ)
    (hp : 0 ≤ p) (hp₁ : p ≤ 1) (hq : 0 ≤ q) (hq₁ : q ≤ 1) :
    0 ≤ p*q ∧ p*q ≤ 1 := by
  constructor
  · positivity
  · nlinarith [mul_nonneg hp (sub_nonneg.mpr hq₁)]

theorem softmax_shift (x y c : ℝ) :
    Real.exp (x+c)/(Real.exp (x+c)+Real.exp (y+c)) =
      Real.exp x/(Real.exp x+Real.exp y) := by
  rw [Real.exp_add, Real.exp_add]
  have hx := Real.exp_pos x
  have hy := Real.exp_pos y
  have hc := Real.exp_pos c
  field_simp
  ring

theorem attention_convex (u v w : ℝ) (hw : 0 ≤ w) (hw₁ : w ≤ 1)
    (huv : u ≤ v) : u ≤ w*u+(1-w)*v ∧ w*u+(1-w)*v ≤ v := by
  constructor
  · nlinarith [mul_nonneg (sub_nonneg.mpr hw₁) (sub_nonneg.mpr huv)]
  · nlinarith [mul_nonneg hw (sub_nonneg.mpr huv)]

theorem mlp_rank_one (a b c d x y : ℝ) :
    (c*(a*x+b*y), d*(a*x+b*y)) =
      ((c*a)*x+(c*b)*y, (d*a)*x+(d*b)*y) := by
  ext <;> ring

-- Algebra of the noising equation; this does not assert a generative model is correct.
theorem denoising_reconstruction (a b x ε z : ℝ) (ha : a ≠ 0)
    (hz : z=a*x+b*ε) : (z-b*ε)/a=x := by
  rw [hz]
  field_simp

end ThreeBlueOneBrown.NeuralNetworks
