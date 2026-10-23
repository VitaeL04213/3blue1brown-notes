import Mathlib

/-! Companion results, one or more for each linear algebra lesson.
The coordinate formulas use real numbers, not floating-point approximations. -/
namespace ThreeBlueOneBrown.LinearAlgebra

theorem vectors_distribute (a : ℝ) (u v : ℝ × ℝ) :
    a • (u + v) = a • u + a • v := smul_add a u v

theorem coordinates_span (x y : ℝ) :
    (x, y) = x • ((1, 0) : ℝ × ℝ) + y • ((0, 1) : ℝ × ℝ) := by
  ext <;> simp

theorem linear_combination {V W : Type*} [AddCommGroup V] [Module ℝ V]
    [AddCommGroup W] [Module ℝ W] (T : V →ₗ[ℝ] W) (a b : ℝ) (u v : V) :
    T (a • u + b • v) = a • T u + b • T v := by simp

theorem matrix_composition (A B : Matrix (Fin 2) (Fin 2) ℝ) (v : Fin 2 → ℝ) :
    Matrix.mulVec A (Matrix.mulVec B v) = Matrix.mulVec (A * B) v :=
  Matrix.mulVec_mulVec v A B

theorem rotation_preserves_square_norm (x y z : ℝ) :
    (-y)^2 + x^2 + z^2 = x^2 + y^2 + z^2 := by ring

theorem determinant_product (a b c d e f g h : ℝ) :
    (a*e+b*g)*(c*f+d*h) - (a*f+b*h)*(c*e+d*g) =
      (a*d-b*c)*(e*h-f*g) := by ring

theorem kernel_translation (T : (ℝ × ℝ) →ₗ[ℝ] (ℝ × ℝ))
    (x v : ℝ × ℝ) (hv : T v = 0) : T (x+v) = T x := by simp [hv]

theorem projection_surjective :
    Function.Surjective (fun v : ℝ × ℝ × ℝ => (v.1, v.2.1)) := by
  rintro ⟨x,y⟩
  exact ⟨(x,y,0), rfl⟩

theorem dot_linear (a b x y u v : ℝ) :
    a*(x+u)+b*(y+v) = (a*x+b*y)+(a*u+b*v) := by ring

theorem cross_orthogonal (a b c x y z : ℝ) :
    a*(b*z-c*y)+b*(c*x-a*z)+c*(a*y-b*x) = 0 := by ring

theorem scalar_triple_product (a b c x y z u v w : ℝ) :
    u*(b*z-c*y)+v*(c*x-a*z)+w*(a*y-b*x) =
      a*(y*w-z*v)-x*(b*w-c*v)+u*(b*z-c*y) := by ring

theorem cramers_rule (a b c d x y p q : ℝ)
    (h₁ : a*x+b*y=p) (h₂ : c*x+d*y=q) (hdet : a*d-b*c ≠ 0) :
    x=(p*d-b*q)/(a*d-b*c) ∧ y=(a*q-p*c)/(a*d-b*c) := by
  constructor
  · apply (eq_div_iff hdet).2
    nlinarith [congrArg (fun t : ℝ => d*t) h₁,
      congrArg (fun t : ℝ => b*t) h₂]
  · apply (eq_div_iff hdet).2
    nlinarith [congrArg (fun t : ℝ => a*t) h₂,
      congrArg (fun t : ℝ => c*t) h₁]

theorem change_of_basis (e : (ℝ × ℝ) ≃ₗ[ℝ] (ℝ × ℝ))
    (T : (ℝ × ℝ) →ₗ[ℝ] (ℝ × ℝ)) (v : ℝ × ℝ) :
    e (e.symm (T (e v))) = T (e v) := e.apply_symm_apply _

theorem eigenvector_scaling (T : (ℝ × ℝ) →ₗ[ℝ] (ℝ × ℝ))
    (v : ℝ × ℝ) (μ a : ℝ) (hv : T v = μ • v) :
    T (a • v) = μ • (a • v) := by
  simp [hv, smul_smul, mul_comm]

theorem characteristic_centering (a b c d t : ℝ) :
    (t-a)*(t-d)-b*c = (t-(a+d)/2)^2-(((a-d)/2)^2+b*c) := by ring

theorem function_space_distribute (a : ℝ) (f g : ℝ → ℝ) :
    a • (f+g) = a • f+a • g := smul_add a f g

end ThreeBlueOneBrown.LinearAlgebra
