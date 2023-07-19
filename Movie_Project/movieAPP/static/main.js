console.log("Ajax is working now.");
// console.log(env.DB_API_KEY);

// loadmore button
const loadBtn = document.getElementById("btn");
const displayBox = document.getElementById("display-box");
const spinnerBox = document.getElementById("spinner-box");
const alertBox = document.getElementById("alert");
var current_page = 1;

$("#btn").click(function () {
  console.log("Your ajax is working");
  current_page += 1;
  loadmorePost(current_page);
});
function loadmorePost(current_page) {
  $.ajax({
    url: `/loadmorejson/${current_page}`,
    type: "GET",
    success: function (res) {
      const data = res.data.results;
      console.log(res);
      spinnerBox.classList.remove("none-visible");
      setTimeout(() => {
        spinnerBox.classList.add("none-visible");
        data.map((m) => {
          console.log(m);
          console.log(displayBox.innerHTML);
          displayBox.innerHTML += `<div class="card">
            <a href={/movies/${m.id}}><img src=https://image.tmdb.org/t/p/w500${m.poster_path}></a>
          </div>`;
        });
      }, 500);
      if (current_page == res.total_pages) {
        console.log("done");
        alertBox.classList.remove("none-visible");
      }
    },
    error: function (err) {
      console.log(err);
    },
  });
}
