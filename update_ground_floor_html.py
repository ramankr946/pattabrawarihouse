from pathlib import Path

from PIL import Image

import base64, io, re

def encode_image(path, max_px=1800):

        im = Image.open(path)

    im.thumbnail((max_px, max_px))

    if im.mode in ("RGBA", "P"):

                im = im.convert("RGB")

    buf = io.BytesIO()

    im.save(buf, format="JPEG", quality=88, optimize=True)

    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

src_candidates = [

    Path("/mnt/data/patta_barawari_architect_brief_FINAL_FINAL_sizing_fixed.html"),

        Path("/mnt/data/patta_barawari_architect_brief_FINAL_FINAL_restored_upper_floors.html"),

        Path("/mnt/data/patta_barawari_architect_brief_FINAL_FINAL_fixed_floors.html"),

        Path("/mnt/data/patta_barawari_architect_brief_updated_final.html"),

]

src = next((p for p in src_candidates if p.exists()), None)

if src is None:

        raise FileNotFoundError("No source HTML found")

html = src.read_text(encoding="utf-8")

new_ground = Path("/mnt/data/a_high_resolution_architectural_infographic_floo.png")

if not new_ground.exists():

        matches = list(Path("/mnt/data").glob("a_high_resolution_architectural_infographic*.png"))

    if not matches:

                raise FileNotFoundError("New ground floor image not found")

    new_ground = matches[0]

ground_uri = encode_image(new_ground)

# Replace first ground-floor drawing image in the final ground-floor section

html = re.sub(

    r'(<figure class="card wide">\s*<img[^>]*src=")[^"]*("[^>]*alt="Final approved ground floor drawing"[^>]*>)',

        r'\1' + ground_uri + r'\2',

        html,

        count=1,

        flags=re.S

)

# Fallback: replace first card wide image after Final Ground Floor Drawing section

if ground_uri not in html:

        html = re.sub(

            r'(<h2>[^<]*Final Ground Floor Drawing[^<]*</h2>.*?<img[^>]*src=")[^"]*(")',

                    r'\1' + ground_uri + r'\2',

                    html,

                    count=1,

                    flags=re.S

        )

# Caption updates

html = html.replace(

    "Latest approved ground floor: one integrated kitchen zone, pantry entrance from kitchen, solid wall after pantry, family sitting only, glass sitting room, parent bedroom near kitchen, and utility block at the end.",

        "Latest approved ground floor: front garden, entrance corridor, glass sitting room first on right with corridor access, parent bedroom on left with corridor access, modern kitchen connected to traditional kitchen with no wall, pantry/store with direct kitchen access, utility spaces on right, stair lobby at rear-right with corridor access, solid wall before family sitting, rear verandah and rear garden."

)

html = html.replace(

    "Latest approved ground floor direction: one integrated kitchen zone, pantry/store with direct entrance from kitchen, solid wall after pantry, family sitting only, glass sitting room, parent bedroom near kitchen, and utility block at the end.",

        "Latest approved ground floor direction: front garden, entrance corridor, glass sitting room first on right with corridor access, parent bedroom on left with corridor access, kitchen sequence on left, utility/stair sequence on right, solid wall before family sitting, rear verandah and rear garden."

)

# Text updates

html = html.replace(

    "Ground floor bedroom placed closer to the kitchen side so parents can live comfortably without using stairs.",

        "Ground floor parent bedroom on the left side with private access from the entrance corridor; parents can live comfortably without using stairs."

)

html = html.replace(

    "Traditional Himachali kitchen with chulha at floor / raised-platform level; modern support kitchen directly connected; no wall between traditional and modern kitchen; pantry/store immediately adjacent to kitchen with direct entrance from kitchen.",

        "Modern kitchen placed before/next to the traditional kitchen, with no wall between them. Traditional Himachali kitchen includes chulha and floor utensil washing area. Pantry/store sits after the traditional kitchen and has direct access from kitchen."

)

html = html.replace(

    "Kitchen zone including pantry/storage must be separated from sitting area by a solid wall / arch opening / hard partition. Not fully open plan.",

        "A solid wall should separate the entrance corridor/kitchen side from the family sitting area. The family sitting area should feel private and not be visible immediately from the entrance."

)

html = html.replace(

    "Garden-facing enclosed sitting room with minimal furniture; tea / reading / winter sun room.",

        "First room on the right side after entering, with direct access from the corridor and front garden view; tea / reading / winter sun room."

)

html = html.replace(

    "Washing area plus separate toilet and separate bath area placed toward the end/service side. Toilet and bath must have independent entries from a common outside/passage area.",

        "Right-side utility sequence: stair lobby at rear-right with corridor access, separate toilet, separate bath area, washing area and utility/store. Toilet and bath must remain separate rooms."

)

final_note = """

  <div class="note"><b>Latest ground-floor layout note:</b> Front garden → entrance verandah → entrance corridor. Right side starts with glass sitting room with corridor access. Left side has parent bedroom, modern kitchen, traditional kitchen and pantry/store. No wall between modern and traditional kitchen. Stair lobby sits at rear-right with corridor access. Solid wall before family sitting area. Rear verandah and rear garden at the back.</div>

  """

if "Latest ground-floor layout note" not in html:

        idx = html.find("Ground Floor")

    end = html.find("</section>", idx)

    if idx != -1 and end != -1:

                html = html[:end] + final_note + html[end:]

out = Path("/mnt/data/patta_barawari_architect_brief_UPDATED_HTML_final_ground.html")

out.write_text(html, encoding="utf-8")

print(out)
