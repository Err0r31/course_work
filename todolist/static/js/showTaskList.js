let currentPage = 1;
const pageSize = 10;

async function fetchTasks(page = 1) {
  const category = document.getElementById("category-filter").value;

  const params = new URLSearchParams({
    page,
    ...(category && { category }),
  });

  const response = await fetch(`tasks/tasks/?${params}`);
  const data = await response.json();

  const taskList = document.getElementById("task-list");
  const pagination = document.getElementById("pagination");
  taskList.innerHTML = "";
  pagination.innerHTML = "";

  if (!Array.isArray(data.results)) {
    console.error("Ошибка: ожидается массив задач, но получен:", data);
    document.getElementById("no-tasks").style.display = "block";
    return;
  }

  if (data.results.length === 0) {
    document.getElementById("no-tasks").style.display = "block";
  } else {
    data.results.forEach((task) => {
      const taskCard = document.createElement("div");
      taskCard.className = "col d-flex";
      taskCard.innerHTML = `
                <div class="card shadow-sm flex-grow-1">
                    <div class="card-header d-flex justify-content-between">
                        ${
                          task.category
                            ? `<span class="badge" style="background-color: ${task.category.color};">${task.category.name}</span>`
                            : ""
                        }
                        ${
                          task.priority
                            ? `<span class="badge" style="background-color: ${task.priority.color};">${task.priority.level}</span>`
                            : ""
                        }
                    </div>
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start gap-2">
                            <h5 class="card-title">
                                <a href="/tasks/${task.id}/">${task.title}</a>
                            </h5>
                            <span class="badge border border-dark px-3 py-2" style="color: black;">
                                ${
                                  task.status === "pending"
                                    ? "Запланировано"
                                    : task.status === "in_progress"
                                    ? "В процессе"
                                    : "Завершено"
                                }
                            </span>
                        </div>
                        <p class="card-text"><strong>Описание:</strong> ${
                          task.description || "Нет описания"
                        }</p>
                        <p class="card-text"><strong>Срок выполнения:</strong> ${
                          task.due_date
                            ? new Date(task.due_date).toLocaleString()
                            : "Не указан"
                        }</p>
                    </div>
                    <div class="card-footer d-flex justify-content-between gap-1">
                        <div class="d-flex gap-1 align-items-center flex-wrap">
                            ${
                              task.tags.length > 0
                                ? task.tags
                                    .map(
                                      (tag) =>
                                        `<span class="badge" style="background-color: ${tag.color}; color: white;">${tag.name}</span>`
                                    )
                                    .join("")
                                : '<small class="text-muted">Теги отсутствуют</small>'
                            }
                        </div>
                        <div class="d-flex gap-2 flex-wrap flex-shrink-0 align-items-center">
                            <a href="tasks/${
                              task.id
                            }/edit/" class="btn btn-primary btn-sm">Редактировать</a>
                            <form action="/tasks/${
                              task.id
                            }/delete/" method="POST" class="d-inline">
                            ${
                              csrfToken
                                ? `<input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}" />`
                                : ""
                            }
                            <button type="submit" class="btn btn-danger btn-sm">Удалить</button>
                          </form>
                        </div>
                    </div>
                </div>
            `;
      taskList.appendChild(taskCard);
    });

    for (let i = 1; i <= Math.ceil(data.count / pageSize); i++) {
      const li = document.createElement("li");
      li.className = "page-item";
      li.innerHTML = `<a class="page-link" href="#" onclick="fetchTasks(${i})">${i}</a>`;
      pagination.appendChild(li);
    }
  }
}

async function loadFilters() {
  const categoryResponse = await fetch("/tasks/categories/");
  const categories = await categoryResponse.json();
  const categoryFilter = document.getElementById("category-filter");

  categories.results.forEach((category) => {
    const option = document.createElement("option");
    option.value = category.id;
    option.textContent = category.name;
    option.style.color = category.color;
    categoryFilter.appendChild(option);
  });
}

function applyFilters() {
  fetchTasks(1);
}

document.addEventListener("DOMContentLoaded", () => {
  loadFilters();
  fetchTasks(currentPage);
});
