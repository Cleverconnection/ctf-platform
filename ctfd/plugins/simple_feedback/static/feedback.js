document.addEventListener("DOMContentLoaded", () => {
  const originalFetch = window.fetch;

  window.fetch = async (...args) => {
    const response = await originalFetch(...args);

    try {
      const url = args[0];
      if (url.includes("/api/v1/challenges/attempt")) {
        console.log("[Feedback] interceptando /attempt");

        const clonedResp = response.clone();
        clonedResp.json().then((data) => {
          console.log("[Feedback] resposta do attempt:", data);

          if (data && data.data && data.data.status === "correct") {
            console.log("[Feedback] Flag correta detectada!");
            const feedbackModal = new bootstrap.Modal(
              document.getElementById("feedbackModal")
            );
            feedbackModal.show();
          }
        });
      }
    } catch (e) {
      console.warn("[Feedback] erro ao processar attempt:", e);
    }

    return response;
  };

  // Handler do formulário
  const form = document.getElementById("feedback-form");
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const rating = document.getElementById("feedback-rating").value;
      const comment = document.getElementById("feedback-comment").value;

      console.log("[Feedback] Enviado:", { rating, comment });

      // Aqui você pode mandar pro backend (rota Flask) ou salvar no DB
      alert("Obrigado pelo feedback!");

      // Fecha modal
      const modalEl = document.getElementById("feedbackModal");
      const modal = bootstrap.Modal.getInstance(modalEl);
      modal.hide();
      form.reset();
    });
  }
});
