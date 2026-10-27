import SidebarProfile from "./SidebarProfile";

function Sidebar({
  activePage,
  setActivePage,
}) {
  const menuItems = [
    {
      id: "dashboard",
      icon: "🏠",
      label: "Dashboard",
    },
    {
      id: "profile",
      icon: "👤",
      label: "Profile",
    },
    {
      id: "resume",
      icon: "📄",
      label: "Resume",
    },
    {
      id: "assessment",
      icon: "📝",
      label: "Assessment",
    },
    {
      id: "github",
      icon: "💻",
      label: "GitHub",
    },
    {
      id: "analytics",
      icon: "📊",
      label: "Analytics",
    },
    {
      id: "recommendations",
      label: "Recommendations",
      icon: "🎯",
    },
  ];

  return (
    <aside className="fixed left-0 top-0 z-50 flex h-screen w-64 flex-col border-r border-slate-800 bg-slate-950">

      {/* Logo */}

      <div className="border-b border-slate-800 px-6 py-5">

        <h1 className="text-2xl font-bold text-cyan-400">
          SkillPath AI
        </h1>

        <p className="mt-1 text-xs text-slate-500">
          AI Career Readiness
        </p>

      </div>


      {/* Navigation */}

      <nav className="flex-1 px-4 py-6">

        <p className="mb-3 px-3 text-xs font-semibold uppercase tracking-wider text-slate-600">
          Main Menu
        </p>

        <div className="space-y-2">

          {menuItems.map((item) => {

            const active =
              activePage === item.id;

            return (
              <button
                key={item.id}
                onClick={() =>
                  setActivePage(item.id)
                }
                className={`flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium transition ${
                  active
                    ? "bg-cyan-400 text-slate-950"
                    : "text-slate-400 hover:bg-slate-900 hover:text-white"
                }`}
              >

                <span className="text-lg">
                  {item.icon}
                </span>

                <span>
                  {item.label}
                </span>

              </button>
            );

          })}

        </div>


        {/* Settings */}

        <div className="mt-8">

          <p className="mb-3 px-3 text-xs font-semibold uppercase tracking-wider text-slate-600">
            System
          </p>

          <button
            onClick={() =>
              setActivePage("settings")
            }
            className={`flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium transition ${
              activePage === "settings"
                ? "bg-cyan-400 text-slate-950"
                : "text-slate-400 hover:bg-slate-900 hover:text-white"
            }`}
          >

            <span className="text-lg">
              ⚙️
            </span>

            <span>
              Settings
            </span>

          </button>

        </div>

      </nav>


      {/* User */}

      <div className="sidebar-profile-container">
        <SidebarProfile />
      </div>

    </aside>
  );
}

export default Sidebar;