const imgHandIphone = "assets/6eacc115-2a75-4ded-872c-92957c05f133.png";
const imgVector12 = "assets/485f69c1-45fb-4994-97e8-c7c2979266c1.svg";
const imgLayer1 = "assets/c1f8d600-a2f1-49e7-842e-fc42eff62f0b.svg";

export default function Template03SplitPhoneHand16X9() {
  return (
    <div className="relative size-full" data-node-id="547:1400" data-name="template-03-split-phone-hand-16x9">
      <div className="-translate-y-1/2 absolute bg-[#ed5370] h-[1080px] left-0 top-1/2 w-[860px]" data-node-id="547:1401" data-name="photo-right" />
      <div className="absolute h-[1080px] right-0 top-0 w-[1060px]" data-node-id="547:1402">
        <div className="-translate-y-1/2 absolute bg-[#131540] h-[1080px] left-0 top-1/2 w-[1060px]" data-node-id="547:1403" data-name="photo-right" />
        <div className="absolute h-[1262.636px] left-[-110px] mix-blend-soft-light top-[284px] w-[2429.41px]" data-node-id="547:1404">
          <div className="absolute inset-[-9.64%_-1.42%_-9.64%_0]">
            <img alt="" className="block max-w-none size-full" src={imgVector12} />
          </div>
        </div>
        <div className="absolute content-stretch flex flex-col h-[980px] items-center justify-between left-[230px] top-[50px] w-[600px]" data-node-id="547:1405">
          <div className="content-stretch flex flex-col gap-[48px] items-center relative shrink-0 w-[734px]" data-node-id="547:1406" data-name="copy">
            <div className="h-[35px] relative shrink-0 w-[157.198px]" data-node-id="547:1407" data-name="Layer_1">
              <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgLayer1} />
            </div>
            <div className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Bold'] font-bold leading-[0] not-italic relative shrink-0 text-[82.324px] text-center text-white tracking-[-3.293px] w-[600px]" data-node-id="547:1413">
              <p className="leading-none mb-0">Open the app</p>
              <p className="leading-none mb-0">Find it fast</p>
              <p className="leading-none">Make it yours.</p>
            </div>
            <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.3] min-w-full not-italic relative shrink-0 text-[40px] text-[rgba(255,255,255,0.85)] text-center w-[min-content]" data-node-id="547:1414">
              Browse, apply, and start shopping right from your phone.
            </p>
            <div className="bg-[#ed5370] content-stretch flex items-center justify-center overflow-clip px-[64px] py-[32px] relative rounded-[49.5px] shrink-0" data-node-id="547:1415" data-name="Button">
              <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.2] not-italic relative shrink-0 text-[73.91px] text-white whitespace-nowrap" data-node-id="I547:1415;2485:67">
                Leap Forward
              </p>
            </div>
          </div>
          <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.2] not-italic relative shrink-0 text-[#d8d8d8] text-[15px] text-center w-[364.925px]" data-node-id="547:1416">
            Lease-purchase service. Total cost exceeds cash price. Approval required. Not available in MN, NJ, WI, WY. See katapult.com.
          </p>
        </div>
      </div>
      <div className="absolute h-[1607.7px] left-[-101px] top-[19px] w-[974.05px]" data-node-id="547:1417" data-name="hand-iphone">
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <img alt="" className="absolute h-[133.91%] left-0 max-w-none top-[-33.91%] w-[147.38%]" src={imgHandIphone} />
        </div>
      </div>
    </div>
  );
}