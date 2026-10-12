function Navbar({ title }) {
  return (
    <nav>
      <h2>{ title }</h2>

      <div>
        <button>Dashboard</button>
        <button>Stocks</button>
        <button>Portfolio</button>
        <button>Alerts</button>
      </div>
    </nav>
  )
}

export default Navbar