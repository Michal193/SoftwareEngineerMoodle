import React from "react";

const APPROACHING_WINDOW_MS = 48 * 60 * 60 * 1000;

function getDueMeta(dueDateStr) {
  if (!dueDateStr) {
    return { level: "normal", label: "No due date", formatted: "No deadline" };
  }

  const dueTime = new Date(dueDateStr).getTime();
  if (Number.isNaN(dueTime)) {
    return { level: "normal", label: "Due date", formatted: dueDateStr };
  }

  const diffMs = dueTime - Date.now();
  const formatted = new Intl.DateTimeFormat(undefined, {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(dueTime));

  if (diffMs < 0) {
    return { level: "overdue", label: "Overdue", formatted };
  }
  if (diffMs <= APPROACHING_WINDOW_MS) {
    return { level: "approaching", label: "Due Soon", formatted };
  }
  return { level: "normal", label: "Upcoming", formatted };
}

function getCardStyles(level) {
  if (level === "overdue") {
    return {
      border: "1px solid #ef4444",
      backgroundColor: "#fef2f2",
      badgeBg: "#fee2e2",
      badgeColor: "#b91c1c",
    };
  }
  if (level === "approaching") {
    return {
      border: "1px solid #f59e0b",
      backgroundColor: "#fffbeb",
      badgeBg: "#fef3c7",
      badgeColor: "#b45309",
    };
  }
  return {
    border: "1px solid #e5e7eb",
    backgroundColor: "#ffffff",
    badgeBg: "#f3f4f6",
    badgeColor: "#374151",
  };
}

export default function AssignmentList({
  tasks = [],
  onComplete,
  completingIds = [],
  loading = false,
  error = null,
}) {
  if (loading) {
    return <p style={{ color: "#6b7280" }}>Loading open assignments...</p>;
  }

  if (error) {
    return (
      <div
        role="alert"
        style={{
          padding: "12px 14px",
          borderRadius: "8px",
          backgroundColor: "#fef2f2",
          border: "1px solid #fecaca",
          color: "#991b1b",
        }}
      >
        {error}
      </div>
    );
  }

  const openTasks = tasks.filter((t) => t.status !== "completed");

  if (openTasks.length === 0) {
    return (
      <div
        style={{
          padding: "20px",
          borderRadius: "8px",
          border: "1px dashed #d1d5db",
          color: "#6b7280",
          textAlign: "center",
        }}
      >
        No open assignments right now.
      </div>
    );
  }

  return (
    <ul
      style={{
        listStyle: "none",
        padding: 0,
        margin: 0,
        display: "flex",
        flexDirection: "column",
        gap: "10px",
      }}
    >
      {openTasks.map((task) => {
        const dueMeta = getDueMeta(task.due_date);
        const styles = getCardStyles(dueMeta.level);
        const isCompleting = completingIds.includes(task.id);

        return (
          <li
            key={task.id}
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              gap: "12px",
              padding: "12px 16px",
              borderRadius: "8px",
              border: styles.border,
              backgroundColor: styles.backgroundColor,
            }}
          >
            <div style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "8px", flexWrap: "wrap" }}>
                <strong>{task.title}</strong>
                <span
                  style={{
                    fontSize: "12px",
                    fontWeight: 600,
                    padding: "2px 8px",
                    borderRadius: "999px",
                    backgroundColor: styles.badgeBg,
                    color: styles.badgeColor,
                  }}
                >
                  {dueMeta.label}
                </span>
                <span
                  style={{
                    fontSize: "12px",
                    padding: "2px 8px",
                    borderRadius: "999px",
                    backgroundColor: "#eef2ff",
                    color: "#3730a3",
                  }}
                >
                  {task.course_id}
                </span>
              </div>

              <div style={{ fontSize: "13px", color: "#4b5563" }}>
                Due: <span>{dueMeta.formatted}</span> · Status:{" "}
                <span>{task.status.replace("_", " ")}</span>
              </div>
            </div>

            <button
              type="button"
              disabled={isCompleting || !onComplete}
              onClick={() => onComplete && onComplete(task.id)}
              style={{
                padding: "8px 12px",
                borderRadius: "6px",
                border: "1px solid #16a34a",
                backgroundColor: isCompleting ? "#86efac" : "#16a34a",
                color: "#ffffff",
                fontWeight: 600,
                cursor: isCompleting ? "not-allowed" : "pointer",
                whiteSpace: "nowrap",
              }}
            >
              {isCompleting ? "Completing..." : "Mark Done"}
            </button>
          </li>
        );
      })}
    </ul>
  );
}