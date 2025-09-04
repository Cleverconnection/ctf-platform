document.addEventListener("DOMContentLoaded", () => {
  const modalEl = document.getElementById("feedbackModal");
  const form = document.getElementById("feedback-form");

  // Função para abrir o modal
  function showFeedbackModal(challengeId) {
    if (!modalEl) return;
    document.getElementById("feedback-challenge-id").value = challengeId;
    const modal = new bootstrap.Modal(modalEl);
    modal.show();
  }

  // Observa mudanças na área de notificações (onde aparece "Correct")
  const observerTarget = document.querySelector("#challenge-window .notification-row");
  if (observerTarget) {
    const observer = new MutationObserver(() => {
      const alert = observerTarget.querySelector(".alert-success strong");
      if (alert && alert.textContent.includes("Correct")) {
        const challengeId = document.querySelector("#challenge-id")?.value;
        if (challengeId) {
          showFeedbackModal(challengeId);
        }
      }
    });

    observer.observe(observerTarget, { childList: true, subtree: true });
  }

  // Envio do feedback
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const payload = {
        challenge_id: document.getElementById("feedback-challenge-id").value,
        rating: document.getElementById("feedback-rating").value,
        comment: document.getElementById("feedback-comment").value
      };

      try {
        const resp = await fetch("/feedback/submit", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        const data = await resp.json();

        alert(data.message || "Feedback enviado!");
        bootstrap.Modal.getInstance(modalEl).hide();
        form.reset();
      } catch (err) {
        console.error("Erro ao enviar feedback:", err);
        alert("Falha ao enviar feedback.");
      }
    });
  }
});
