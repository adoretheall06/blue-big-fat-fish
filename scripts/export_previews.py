"""Export animation GIFs from the existing Pets v2 atlas pixels."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
STATES = [('idle', 6), ('running-right', 8), ('running-left', 8),
          ('waving', 4), ('jumping', 5), ('failed', 8),
          ('waiting', 6), ('running', 6), ('review', 6)]

def main():
    atlas = Image.open(ROOT / 'final/spritesheet-extended.png').convert('RGBA')
    if atlas.size != (1536, 2288):
        raise ValueError('Expected a 1536 x 2288 Pets v2 atlas')
    output = ROOT / 'exports'
    output.mkdir(exist_ok=True)
    def frame(row, col):
        return atlas.crop((col * 192, row * 208, (col + 1) * 192, (row + 1) * 208))
    def save(name, frames, duration=150):
        frames[0].save(output / f'{name}.gif', save_all=True,
                       append_images=frames[1:], duration=duration,
                       loop=0, disposal=2, optimize=False)
    for row, (name, count) in enumerate(STATES):
        save(name, [frame(row, col) for col in range(count)])
    save('look-loop', [frame(9 + index // 8, index % 8) for index in range(16)], 160)
    save('idle-jump-idle', [frame(0, c) for c in range(6)] +
         [frame(4, c) for c in range(5)] + [frame(0, c) for c in range(6)])
    print(f'Exported 11 GIF previews to {output}')

if __name__ == '__main__':
    main()
