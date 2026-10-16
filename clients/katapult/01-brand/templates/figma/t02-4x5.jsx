const imgPhotoRight = "assets/ccbaaea2-3ce4-4fd7-8769-9a7f4f949c9d.png";
const imgLayer1 = "assets/a9216b16-eb4e-4b3f-b8f2-0f6baf20b226.svg";

export default function Template02SplitPanelImage4X5() {
  return (
    <div className="relative size-full" data-node-id="547:1337" data-name="template-02-split-panel-image-4x5">
      <div className="-translate-y-1/2 absolute bg-[#131540] h-[1350px] left-0 top-1/2 w-[585px]" data-node-id="547:1338" data-name="photo-right" />
      <div className="-translate-y-1/2 absolute h-[1350px] right-0 top-1/2 w-[495px]" data-node-id="547:1339" data-name="photo-right">
        <div aria-hidden className="absolute inset-0 pointer-events-none">
          <img alt="" className="absolute max-w-none object-cover size-full" src={imgPhotoRight} />
          <div className="absolute bg-[rgba(0,0,0,0.2)] inset-0" />
        </div>
      </div>
      <div className="absolute content-stretch flex flex-col gap-[48px] items-start left-[48px] top-[88px] w-[505px]" data-node-id="547:1340" data-name="copy">
        <div className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Bold'] font-bold leading-[0] not-italic relative shrink-0 text-[88px] text-white tracking-[-3.52px] w-[505px]" data-node-id="547:1341">
          <p className="leading-[0.9] mb-0">Your home.</p>
          <p className="leading-[0.9] mb-0">Your upgrade.</p>
          <p className="leading-[0.9]">Your move.</p>
        </div>
        <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.3] not-italic relative shrink-0 text-[40px] text-[rgba(255,255,255,0.85)] w-[505px]" data-node-id="547:1342">
          New couch, new laptop, new fridge. No credit score required.
        </p>
        <div className="bg-[#ed5370] content-stretch flex items-center justify-center overflow-clip px-[64px] py-[32px] relative rounded-[49.5px] shrink-0" data-node-id="547:1343" data-name="Button">
          <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.2] not-italic relative shrink-0 text-[73.91px] text-white whitespace-nowrap" data-node-id="I547:1343;2485:67">
            Leap Forward
          </p>
        </div>
      </div>
      <div className="absolute bottom-[46px] content-stretch flex flex-col h-[101px] items-start justify-between left-[48px]" data-node-id="547:1344">
        <div className="h-[35px] relative shrink-0 w-[157.198px]" data-node-id="547:1345" data-name="Layer_1">
          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgLayer1} />
        </div>
        <div className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[0] not-italic relative shrink-0 text-[#d8d8d8] text-[15px] w-[541px]" data-node-id="547:1351">
          <p className="leading-[1.2] mb-0">Lease-purchase service. Total cost exceeds cash price.</p>
          <p className="leading-[1.2]">Approval required. Not available in MN, NJ, WI, WY. See katapult.com.</p>
        </div>
      </div>
    </div>
  );
}