import { useAuth } from "../context/AuthContext";
import "../styles/SidebarProfile.css";

export default function SidebarProfile() {
  const { user } = useAuth();

  const name =
    user?.name ||
    user?.full_name ||
    user?.username ||
    user?.email?.split("@")[0] ||
    "Student";

  const initial = name.trim().charAt(0).toUpperCase() || "S";

  return (
    <div className="sp-sidebar-profile">
      <div className="sp-sidebar-avatar" aria-hidden="true">
        {initial}
      </div>

      <div className="sp-sidebar-user-details">
        <span className="sp-sidebar-user-name" title={name}>
          {name}
        </span>
        <span className="sp-sidebar-user-role">SkillPath AI Student</span>
      </div>

      <div className="sp-sidebar-status" title="Signed in" />
    </div>
  );
}
