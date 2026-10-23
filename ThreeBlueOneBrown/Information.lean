import Mathlib

namespace ThreeBlueOneBrown.Information
noncomputable section

def entropyTerm (p : ℝ) : ℝ := -p*Real.log p

theorem entropy_term_nonnegative (p : ℝ) (hp : 0<p) (hp₁ : p≤1) :
    0 ≤ entropyTerm p := by
  unfold entropyTerm
  have hl : Real.log p ≤ 0 := Real.log_nonpos hp.le hp₁
  exact mul_nonneg_of_nonpos_of_nonpos (neg_nonpos.mpr hp.le) hl

def entropy {n : ℕ} (p : Fin n → ℝ) : ℝ := ∑ i, -p i*Real.log (p i)
def crossEntropy {n : ℕ} (p q : Fin n → ℝ) : ℝ := ∑ i, -p i*Real.log (q i)
def klDivergence {n : ℕ} (p q : Fin n → ℝ) : ℝ :=
  ∑ i, p i*Real.log (p i/q i)

theorem cross_entropy_decomposition {n : ℕ} (p q : Fin n → ℝ)
    (hp : ∀ i, 0 < p i) (hq : ∀ i, 0 < q i) :
    crossEntropy p q = entropy p + klDivergence p q := by
  unfold crossEntropy entropy klDivergence
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro i _
  rw [Real.log_div (ne_of_gt (hp i)) (ne_of_gt (hq i))]
  ring

theorem kl_nonnegative {n : ℕ} (p q : Fin n → ℝ)
    (hp : ∀ i, 0 < p i) (hq : ∀ i, 0 < q i)
    (hpn : ∑ i, p i = 1) (hqn : ∑ i, q i = 1) :
    0 ≤ klDivergence p q := by
  have hbound : ∀ i, p i-q i ≤ p i*Real.log (p i/q i) := by
    intro i
    have hl := Real.log_le_sub_one_of_pos (div_pos (hq i) (hp i))
    have hm := mul_le_mul_of_nonneg_left hl (hp i).le
    have heq : p i*(q i/p i-1)=q i-p i := by
      field_simp [ne_of_gt (hp i)]
    rw [heq, Real.log_div (ne_of_gt (hq i)) (ne_of_gt (hp i))] at hm
    rw [Real.log_div (ne_of_gt (hp i)) (ne_of_gt (hq i))]
    nlinarith
  have hs := Finset.sum_le_sum (fun i (_ : i ∈ Finset.univ) => hbound i)
  simpa [klDivergence, Finset.sum_sub_distrib, hpn, hqn] using hs

end
end ThreeBlueOneBrown.Information
